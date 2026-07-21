"""Thread-safe connector metadata and implementation registry."""

from dataclasses import replace
from threading import RLock

from .connector import BaseConnector
from .enums import ErrorCode
from .errors import CollaborationConnectivityError


class ConnectorRegistry:
    def __init__(self) -> None:
        self._connectors: dict[str, BaseConnector] = {}
        self._lock = RLock()

    def register(self, connector: BaseConnector) -> None:
        connector_id = connector.metadata.connector_id
        with self._lock:
            if connector_id in self._connectors:
                raise ValueError(f"connector already registered: {connector_id}")
            self._connectors[connector_id] = connector

    def get(self, connector_id: str, *, require_enabled: bool = False) -> BaseConnector:
        connector = self._connectors.get(connector_id)
        if connector is None:
            raise CollaborationConnectivityError(ErrorCode.CONNECTOR_NOT_FOUND, f"Connector not found: {connector_id}")
        if require_enabled and not connector.metadata.enabled:
            raise CollaborationConnectivityError(ErrorCode.CONNECTOR_DISABLED, f"Connector is disabled: {connector_id}")
        return connector

    def set_enabled(self, connector_id: str, enabled: bool) -> None:
        with self._lock:
            connector = self.get(connector_id)
            connector.metadata = replace(connector.metadata, enabled=enabled)

    def list_connectors(self) -> tuple[object, ...]:
        return tuple(self._connectors[key].metadata for key in sorted(self._connectors))

    def supports(self, connector_id: str, operation: str) -> bool:
        return operation in self.get(connector_id).metadata.supported_operations

    def __len__(self) -> int:
        return len(self._connectors)
