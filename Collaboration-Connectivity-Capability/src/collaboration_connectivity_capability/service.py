"""Governed connection orchestration across replaceable providers."""

from __future__ import annotations

import json
from concurrent.futures import ThreadPoolExecutor, TimeoutError as FutureTimeoutError
from dataclasses import replace
from time import perf_counter
from typing import Any

from .contracts import EnhancementGateway, SafetyAssessment, SafetyGateway
from .enums import ErrorCode
from .errors import CollaborationConnectivityError
from .execution import ExecutionRecorder, sanitize_metadata
from .models import (
    CAPABILITY_VERSION,
    CollaborationConnectivityExecutionRecord,
    ConnectionRequest,
    ConnectionResponse,
    new_id,
    utc_now,
)
from .registry import ConnectorRegistry


class DefaultSafetyGateway:
    """Conservative local validation; replace through the public SafetyGateway."""

    def __init__(self, *, maximum_payload_bytes: int = 1_000_000) -> None:
        self.maximum_payload_bytes = maximum_payload_bytes

    def validate_request(self, request: ConnectionRequest, *, connector_enabled: bool, supported: bool) -> SafetyAssessment:
        try:
            request.validate()
        except (TypeError, ValueError) as exc:
            return SafetyAssessment(False, str(exc), "HIGH")
        if not connector_enabled:
            return SafetyAssessment(False, "Connector is disabled", "HIGH")
        if not supported:
            return SafetyAssessment(False, "Operation is not allowed by the connector contract", "MEDIUM")
        try:
            size = len(json.dumps(request.payload, default=str).encode("utf-8"))
        except (TypeError, ValueError):
            return SafetyAssessment(False, "Payload cannot be safely serialized", "MEDIUM")
        if size > self.maximum_payload_bytes:
            return SafetyAssessment(False, "Payload exceeds the configured safety limit", "HIGH")
        risk_level = str(request.metadata.get("risk_level", "LOW")).upper()
        if risk_level == "CRITICAL":
            return SafetyAssessment(False, "Critical-risk external execution is blocked", "CRITICAL")
        return SafetyAssessment(True, risk_level=risk_level)

    def validate_response(self, request: ConnectionRequest, response: ConnectionResponse) -> SafetyAssessment:
        if response.request_id != request.request_id or response.connector_id != request.connector_id:
            return SafetyAssessment(False, "Response identity does not match the request", "HIGH")
        return SafetyAssessment(True)

    def recover(self, request: ConnectionRequest, error: Exception) -> dict[str, Any]:
        return {"available": True, "strategy": "safe-stop", "request_id": request.request_id}


class NullEnhancementGateway:
    def record_connection_result(self, response: ConnectionResponse) -> None:
        return None


class CollaborationConnectivityService:
    def __init__(
        self,
        *,
        registry: ConnectorRegistry | None = None,
        recorder: ExecutionRecorder | None = None,
        safety_gateway: SafetyGateway | None = None,
        enhancement_gateway: EnhancementGateway | None = None,
    ) -> None:
        self.registry = registry or ConnectorRegistry()
        self.recorder = recorder or ExecutionRecorder()
        self.safety_gateway = safety_gateway or DefaultSafetyGateway()
        self.enhancement_gateway = enhancement_gateway or NullEnhancementGateway()

    def execute(self, request: ConnectionRequest) -> ConnectionResponse:
        if not isinstance(request, ConnectionRequest):
            raise TypeError("request must be a ConnectionRequest")
        started = perf_counter()
        retries = 0
        recovery_result: str | None = None
        try:
            try:
                request.validate()
            except (TypeError, ValueError) as exc:
                raise CollaborationConnectivityError(ErrorCode.INVALID_REQUEST, str(exc)) from exc
            connector = self.registry.get(request.connector_id)
            supported = request.operation in connector.metadata.supported_operations
            assessment = self.safety_gateway.validate_request(request, connector_enabled=connector.metadata.enabled, supported=supported)
            if not assessment.allowed:
                code = ErrorCode.CONNECTOR_DISABLED if not connector.metadata.enabled else ErrorCode.UNSUPPORTED_OPERATION if not supported else ErrorCode.SAFETY_REJECTED
                raise CollaborationConnectivityError(code, assessment.reason)
            operation = getattr(connector, request.operation, None)
            if operation is None or request.operation == "health_check":
                if request.operation == "health_check" and supported:
                    operation = connector.health_check
                else:
                    raise CollaborationConnectivityError(ErrorCode.UNSUPPORTED_OPERATION, f"Unsupported operation: {request.operation}")
            timeout = request.timeout_seconds or connector.metadata.timeout_seconds
            max_attempts = connector.metadata.retry_policy.max_attempts
            while True:
                try:
                    executor = ThreadPoolExecutor(max_workers=1)
                    future = executor.submit(operation) if request.operation == "health_check" else executor.submit(operation, request)
                    try:
                        data = future.result(timeout=timeout)
                    finally:
                        executor.shutdown(wait=False, cancel_futures=True)
                    break
                except FutureTimeoutError as exc:
                    error = CollaborationConnectivityError(ErrorCode.TIMEOUT, f"Connector timed out after {timeout:g} seconds", retryable=True)
                    if retries + 1 >= max_attempts:
                        raise error from exc
                    retries += 1
                except CollaborationConnectivityError as exc:
                    if not exc.retryable or exc.code.value not in connector.metadata.retry_policy.retryable_errors or retries + 1 >= max_attempts:
                        raise
                    retries += 1
            response = ConnectionResponse(request.request_id, request.connector_id, True, "SUCCESS", data=data, execution_time_ms=(perf_counter() - started) * 1000, metadata={"correlation_id": request.correlation_id})
            response_assessment = self.safety_gateway.validate_response(request, response)
            if not response_assessment.allowed:
                raise CollaborationConnectivityError(ErrorCode.INVALID_RESPONSE, response_assessment.reason)
        except CollaborationConnectivityError as exc:
            response = ConnectionResponse(request.request_id, request.connector_id, False, "FAILED", error_code=exc.code.value, error_message=str(exc), execution_time_ms=(perf_counter() - started) * 1000, retryable=exc.retryable, metadata={"correlation_id": request.correlation_id})
        except Exception as exc:
            recovery = self.safety_gateway.recover(request, exc)
            recovery_result = str(recovery.get("strategy", "safe-stop"))
            response = ConnectionResponse(request.request_id, request.connector_id, False, "FAILED", error_code=ErrorCode.INTERNAL_ERROR.value, error_message="Connector execution failed safely", execution_time_ms=(perf_counter() - started) * 1000, metadata={"correlation_id": request.correlation_id})
        self._record(request, response, retries, recovery_result)
        analysis_response = replace(response, data=None, metadata=sanitize_metadata(response.metadata))
        self.enhancement_gateway.record_connection_result(analysis_response)
        return response

    def execute_connector_request(self, request: ConnectionRequest) -> ConnectionResponse:
        """Automation-facing adapter method."""
        return self.execute(request)

    def health_check(self) -> dict[str, object]:
        from .health import check_all, overall_status

        results = check_all(self.registry)
        return {"capability": "Collaboration & Connectivity", "version": CAPABILITY_VERSION, "status": overall_status(results), "connectors": results}

    def _record(self, request: ConnectionRequest, response: ConnectionResponse, retries: int, recovery_result: str | None) -> None:
        self.recorder.record(CollaborationConnectivityExecutionRecord(
            execution_id=new_id("execution"), capability="collaboration-connectivity", connector_id=request.connector_id,
            operation=request.operation, source=request.source, target=request.target, success=response.success,
            status=response.status, error_code=response.error_code, execution_time_ms=response.execution_time_ms,
            retry_count=retries, recovery_result=recovery_result, version=CAPABILITY_VERSION, timestamp=utc_now(),
            metadata=sanitize_metadata({"correlation_id": request.correlation_id, **request.metadata}),
        ))
