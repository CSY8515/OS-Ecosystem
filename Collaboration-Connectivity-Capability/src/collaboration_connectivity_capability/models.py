"""Immutable request, response, health, messaging, and synchronization models."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from typing import Any
from uuid import uuid4

from .enums import ConnectorStatus, ConnectorType, HealthStatus, MessageStatus, SyncStatus

CAPABILITY_VERSION = "1.0.0"


def utc_now() -> datetime:
    return datetime.now(UTC)


def new_id(prefix: str) -> str:
    return f"{prefix}-{uuid4().hex}"


@dataclass(frozen=True, slots=True)
class RetryPolicy:
    max_attempts: int = 1
    retryable_errors: frozenset[str] = frozenset({"TIMEOUT", "RATE_LIMITED", "EXTERNAL_SERVICE_UNAVAILABLE"})

    def __post_init__(self) -> None:
        if self.max_attempts < 1 or self.max_attempts > 10:
            raise ValueError("max_attempts must be between 1 and 10")


@dataclass(frozen=True, slots=True)
class ConnectorMetadata:
    connector_id: str
    name: str
    connector_type: ConnectorType
    provider: str
    version: str
    status: ConnectorStatus = ConnectorStatus.REGISTERED
    supported_operations: frozenset[str] = frozenset()
    authentication_type: str = "NONE"
    endpoint_type: str = "LOCAL"
    timeout_seconds: float = 30.0
    retry_policy: RetryPolicy = field(default_factory=RetryPolicy)
    enabled: bool = True
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.connector_id.strip() or not self.name.strip():
            raise ValueError("connector_id and name are required")
        if self.timeout_seconds <= 0:
            raise ValueError("timeout_seconds must be positive")


@dataclass(frozen=True, slots=True)
class ConnectionRequest:
    connector_id: str
    operation: str
    source: str
    target: str
    payload: Any = None
    headers: dict[str, str] = field(default_factory=dict)
    metadata: dict[str, Any] = field(default_factory=dict)
    timeout_seconds: float | None = None
    request_id: str = field(default_factory=lambda: new_id("request"))
    created_at: datetime = field(default_factory=utc_now)
    correlation_id: str = field(default_factory=lambda: new_id("correlation"))

    def validate(self) -> None:
        for name, value in (("connector_id", self.connector_id), ("operation", self.operation), ("source", self.source), ("target", self.target)):
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"{name} is required")
        if self.timeout_seconds is not None and self.timeout_seconds <= 0:
            raise ValueError("timeout_seconds must be positive")


@dataclass(frozen=True, slots=True)
class ConnectionResponse:
    request_id: str
    connector_id: str
    success: bool
    status: str
    data: Any = None
    error_code: str | None = None
    error_message: str | None = None
    execution_time_ms: float = 0.0
    retryable: bool = False
    timestamp: datetime = field(default_factory=utc_now)
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        item = asdict(self)
        item["timestamp"] = self.timestamp.isoformat()
        return item


@dataclass(frozen=True, slots=True)
class ConnectorHealthResult:
    connector_id: str
    status: HealthStatus
    availability: bool
    latency_ms: float = 0.0
    authentication_state: str = "NOT_REQUIRED"
    last_success: datetime | None = None
    last_failure: datetime | None = None
    consecutive_failures: int = 0
    degraded: bool = False
    retry_recommended: bool = False
    message: str = ""
    checked_at: datetime = field(default_factory=utc_now)


@dataclass(frozen=True, slots=True)
class ImportRequest:
    content: str | bytes
    format: str
    schema: dict[str, type | tuple[type, ...]] | None = None
    transformation_rules: tuple["TransformationRule", ...] = ()


@dataclass(frozen=True, slots=True)
class ImportResult:
    success: bool
    records: tuple[Any, ...] = ()
    processed_count: int = 0
    failure_count: int = 0
    errors: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class ExportRequest:
    records: tuple[Any, ...]
    format: str
    schema: dict[str, type | tuple[type, ...]] | None = None
    transformation_rules: tuple["TransformationRule", ...] = ()


@dataclass(frozen=True, slots=True)
class ExportResult:
    success: bool
    content: str = ""
    exported_count: int = 0
    errors: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class TransformationRule:
    operation: str
    source: str | None = None
    target: str | None = None
    value: Any = None
    target_type: str | None = None


@dataclass(frozen=True, slots=True)
class TransformationResult:
    success: bool
    data: dict[str, Any]
    applied_count: int = 0
    errors: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class CollaborationMessage:
    message_type: str
    source: str
    target: str
    payload: Any
    priority: int = 0
    expires_at: datetime | None = None
    correlation_id: str = field(default_factory=lambda: new_id("correlation"))
    metadata: dict[str, Any] = field(default_factory=dict)
    message_id: str = field(default_factory=lambda: new_id("message"))
    created_at: datetime = field(default_factory=utc_now)


@dataclass(frozen=True, slots=True)
class MessageResult:
    message_id: str
    status: MessageStatus
    success: bool
    error_code: str | None = None
    message: str = ""


@dataclass(frozen=True, slots=True)
class SyncRequest:
    connector_id: str
    source: str
    target: str
    items: tuple[Any, ...] = ()
    metadata: dict[str, Any] = field(default_factory=dict)
    sync_id: str = field(default_factory=lambda: new_id("sync"))


@dataclass(frozen=True, slots=True)
class SyncRecord:
    sync_id: str
    connector_id: str
    source: str
    target: str
    started_at: datetime
    completed_at: datetime | None = None
    status: SyncStatus = SyncStatus.PENDING
    processed_count: int = 0
    success_count: int = 0
    failure_count: int = 0
    conflict_count: int = 0
    error_code: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class CollaborationConnectivityExecutionRecord:
    execution_id: str
    capability: str
    connector_id: str
    operation: str
    source: str
    target: str
    success: bool
    status: str
    error_code: str | None
    execution_time_ms: float
    retry_count: int
    recovery_result: str | None
    version: str
    timestamp: datetime
    metadata: dict[str, Any] = field(default_factory=dict)
