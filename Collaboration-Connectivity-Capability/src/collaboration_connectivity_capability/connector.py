"""Base connector contract and deterministic in-memory implementation."""

from __future__ import annotations

from abc import ABC
from typing import Any, Callable

from .errors import CollaborationConnectivityError, UnsupportedOperationError
from .enums import ConnectorStatus, ErrorCode, HealthStatus
from .models import ConnectionRequest, ConnectorHealthResult, ConnectorMetadata


class BaseConnector(ABC):
    def __init__(self, metadata: ConnectorMetadata) -> None:
        self.metadata = metadata

    def _unsupported(self, operation: str) -> Any:
        raise UnsupportedOperationError(operation)

    def connect(self, request: ConnectionRequest) -> Any: return self._unsupported("connect")
    def disconnect(self, request: ConnectionRequest) -> Any: return self._unsupported("disconnect")
    def health_check(self) -> ConnectorHealthResult:
        if not self.metadata.enabled:
            return ConnectorHealthResult(self.metadata.connector_id, HealthStatus.DISABLED, False, message="Connector is disabled")
        return ConnectorHealthResult(self.metadata.connector_id, HealthStatus.UNKNOWN, False, message="Health check is unsupported")
    def send(self, request: ConnectionRequest) -> Any: return self._unsupported("send")
    def receive(self, request: ConnectionRequest) -> Any: return self._unsupported("receive")
    def import_data(self, request: ConnectionRequest) -> Any: return self._unsupported("import_data")
    def export_data(self, request: ConnectionRequest) -> Any: return self._unsupported("export_data")
    def get_status(self, request: ConnectionRequest) -> Any:
        return {"status": self.metadata.status.value, "enabled": self.metadata.enabled}


class InMemoryConnector(BaseConnector):
    """Test/demo connector with no network or credential dependencies."""

    def __init__(self, metadata: ConnectorMetadata, handlers: dict[str, Callable[[ConnectionRequest], Any]] | None = None) -> None:
        super().__init__(metadata)
        self.handlers = dict(handlers or {})
        self.connected = False
        self.messages: list[Any] = []

    def _run(self, operation: str, request: ConnectionRequest) -> Any:
        if operation not in self.metadata.supported_operations:
            return self._unsupported(operation)
        handler = self.handlers.get(operation)
        if handler:
            return handler(request)
        if operation == "connect": self.connected = True; return {"connected": True}
        if operation == "disconnect": self.connected = False; return {"connected": False}
        if operation == "send": self.messages.append(request.payload); return {"accepted": True, "message_count": len(self.messages)}
        if operation == "receive": return list(self.messages)
        if operation in {"import_data", "export_data"}: return request.payload
        if operation == "get_status": return {"status": ConnectorStatus.AVAILABLE.value, "enabled": True}
        return self._unsupported(operation)

    def connect(self, request: ConnectionRequest) -> Any: return self._run("connect", request)
    def disconnect(self, request: ConnectionRequest) -> Any: return self._run("disconnect", request)
    def send(self, request: ConnectionRequest) -> Any: return self._run("send", request)
    def receive(self, request: ConnectionRequest) -> Any: return self._run("receive", request)
    def import_data(self, request: ConnectionRequest) -> Any: return self._run("import_data", request)
    def export_data(self, request: ConnectionRequest) -> Any: return self._run("export_data", request)
    def get_status(self, request: ConnectionRequest) -> Any: return self._run("get_status", request)
    def health_check(self) -> ConnectorHealthResult:
        if not self.metadata.enabled:
            return super().health_check()
        return ConnectorHealthResult(self.metadata.connector_id, HealthStatus.HEALTHY, True, authentication_state="READY", message="In-memory connector is available")


def raise_rate_limit(_: ConnectionRequest) -> Any:
    raise CollaborationConnectivityError(ErrorCode.RATE_LIMITED, "Connector rate limit reached", retryable=True)
