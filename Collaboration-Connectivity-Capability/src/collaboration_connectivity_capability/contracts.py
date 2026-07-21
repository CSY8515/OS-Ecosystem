"""Replaceable connector and cross-capability gateway contracts."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Protocol

from .models import ConnectionRequest, ConnectionResponse


@dataclass(frozen=True, slots=True)
class SafetyAssessment:
    allowed: bool = True
    reason: str = "Safety checks passed"
    risk_level: str = "LOW"


class SafetyGateway(Protocol):
    def validate_request(self, request: ConnectionRequest, *, connector_enabled: bool, supported: bool) -> SafetyAssessment: ...
    def validate_response(self, request: ConnectionRequest, response: ConnectionResponse) -> SafetyAssessment: ...
    def recover(self, request: ConnectionRequest, error: Exception) -> dict[str, Any]: ...


class EnhancementGateway(Protocol):
    def record_connection_result(self, response: ConnectionResponse) -> None: ...


class AutomationConnectorGateway(Protocol):
    def execute_connector_request(self, request: ConnectionRequest) -> ConnectionResponse: ...
