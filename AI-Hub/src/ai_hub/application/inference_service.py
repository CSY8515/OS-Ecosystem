from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
import json
import logging
from time import monotonic
from typing import Callable, Mapping
from uuid import uuid4

from ai_hub.application.api_management_service import APIManagementService
from ai_hub.domain.common.errors import ErrorCode, ProviderCallError
from ai_hub.domain.executions import ExecutionAttempt, ExecutionRepository, ExecutionSummary
from ai_hub.domain.providers import InferenceRequest, ProviderAdapter, Usage
from ai_hub.domain.router import Router, RoutingCandidate, RoutingPolicy
from ai_hub.infrastructure.secrets import SecretUnavailableError


logger = logging.getLogger(__name__)


@dataclass(frozen=True, slots=True)
class NormalizedResponse:
    correlation_id: str
    request_id: str
    success: bool
    output_text: str | None
    provider_id: str | None
    model_id: str | None
    duration_ms: float
    attempt_count: int
    routing_policy_version: str
    usage: Usage = Usage()
    failover: bool = False
    error_code: str | None = None
    retryable: bool = False


class InferenceService:
    def __init__(
        self,
        *,
        router: Router,
        adapters: Mapping[object, ProviderAdapter],
        secret_resolver,
        execution_repository: ExecutionRepository,
        api_management: APIManagementService,
        timer: Callable[[], float] = monotonic,
        clock: Callable[[], datetime],
        correlation_factory: Callable[[], str] = lambda: f"corr-{uuid4().hex}",
    ) -> None:
        self._router = router
        self._adapters = dict(adapters)
        self._secrets = secret_resolver
        self._executions = execution_repository
        self._api_management = api_management
        self._timer = timer
        self._clock = clock
        self._correlation_factory = correlation_factory
        self._idempotency: dict[tuple[str, str], NormalizedResponse] = {}

    def execute(
        self,
        request: InferenceRequest,
        candidates: tuple[RoutingCandidate, ...],
        policy: RoutingPolicy,
        *,
        timeout_seconds: float,
        overall_timeout_seconds: float,
    ) -> NormalizedResponse:
        key = (request.caller_id, request.request_id)
        if key in self._idempotency:
            return self._idempotency[key]
        self._api_management.authorize(request.caller_id, "inference")
        correlation_id = self._correlation_factory()
        started = self._timer()
        timestamp = self._clock()
        decision = self._router.route(request, candidates, policy)
        attempts: list[ExecutionAttempt] = []
        result = None
        last_error: ProviderCallError | None = None

        for sequence, scored in enumerate(decision.ordered_candidates, start=1):
            elapsed = self._timer() - started
            remaining = overall_timeout_seconds - elapsed
            if remaining <= 0:
                last_error = ProviderCallError(ErrorCode.TIMEOUT, "AI Hub request deadline reached", retryable=True)
                break
            candidate = scored.candidate
            attempt_started = self._timer()
            try:
                credential = self._secrets.resolve(candidate.provider.secret_reference)
                adapter = self._adapters[candidate.provider.family]
                provider_result = adapter.execute(
                    request, candidate.model, credential, min(timeout_seconds, remaining)
                )
                if provider_result.provider != candidate.provider.family:
                    raise ProviderCallError(ErrorCode.INVALID_PROVIDER_RESPONSE, "provider identity mismatch")
                if request.response_format == "json":
                    try:
                        json.loads(provider_result.output_text)
                    except json.JSONDecodeError:
                        raise ProviderCallError(ErrorCode.INVALID_PROVIDER_RESPONSE, "provider returned invalid JSON") from None
                duration = round(max(0.0, (self._timer() - attempt_started) * 1000), 3)
                attempts.append(ExecutionAttempt(
                    correlation_id, sequence, self._clock(), candidate.provider.provider_id,
                    candidate.model.model_id, request.task_kind, duration, True, retry=sequence > 1,
                ))
                result = provider_result
                break
            except SecretUnavailableError:
                error = ProviderCallError(ErrorCode.CREDENTIAL_UNAVAILABLE, "provider credential is unavailable")
            except KeyError:
                error = ProviderCallError(ErrorCode.PROVIDER_UNAVAILABLE, "provider adapter is unavailable")
            except ProviderCallError as provider_error:
                error = provider_error
            duration = round(max(0.0, (self._timer() - attempt_started) * 1000), 3)
            last_error = error
            attempts.append(ExecutionAttempt(
                correlation_id, sequence, self._clock(), candidate.provider.provider_id,
                candidate.model.model_id, request.task_kind, duration, False,
                error_code=str(error.code), retry=sequence > 1,
            ))
            if not error.retryable:
                break

        total_duration = round(max(0.0, (self._timer() - started) * 1000), 3)
        if result is not None:
            selected_attempt = attempts[-1]
            response = NormalizedResponse(
                correlation_id, request.request_id, True, result.output_text,
                selected_attempt.provider_id, selected_attempt.model_id, total_duration,
                len(attempts), decision.policy_version, result.usage, len(attempts) > 1,
            )
        else:
            error = last_error or ProviderCallError(
                ErrorCode.NO_ELIGIBLE_PROVIDER, "no eligible provider is available"
            )
            response = NormalizedResponse(
                correlation_id, request.request_id, False, None, None, None,
                total_duration, len(attempts), decision.policy_version,
                failover=len(attempts) > 1, error_code=str(error.code), retryable=error.retryable,
            )

        summary = ExecutionSummary(
            correlation_id, request.request_id, request.caller_id, timestamp, request.task_kind,
            total_duration, response.success, len(attempts), decision.policy_version,
            provider_id=response.provider_id, model_id=response.model_id, error_code=response.error_code,
            input_units=response.usage.input_units, output_units=response.usage.output_units,
            total_units=response.usage.total_units,
        )
        self._idempotency[key] = response
        try:
            self._executions.record(summary, tuple(attempts))
        except Exception:
            logger.exception("execution_record_write_failed", extra={"correlation_id": correlation_id})
        return response
