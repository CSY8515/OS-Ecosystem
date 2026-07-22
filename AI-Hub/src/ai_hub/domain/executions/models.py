from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True, slots=True)
class ExecutionAttempt:
    correlation_id: str
    sequence: int
    timestamp: datetime
    provider_id: str
    model_id: str
    task_kind: str
    duration_ms: float
    success: bool
    error_code: str | None = None
    retry: bool = False

    def __post_init__(self) -> None:
        if not self.correlation_id or not self.provider_id or not self.model_id:
            raise ValueError("attempt identity is required")
        if self.sequence < 1 or self.duration_ms < 0:
            raise ValueError("attempt sequence and duration are invalid")
        if self.success and self.error_code:
            raise ValueError("successful attempt cannot have an error code")


@dataclass(frozen=True, slots=True)
class ExecutionSummary:
    correlation_id: str
    request_id: str
    caller_id: str
    timestamp: datetime
    task_kind: str
    duration_ms: float
    success: bool
    attempt_count: int
    routing_policy_version: str
    provider_id: str | None = None
    model_id: str | None = None
    error_code: str | None = None
    input_units: int | None = None
    output_units: int | None = None
    total_units: int | None = None

    def __post_init__(self) -> None:
        if not self.correlation_id or not self.request_id or not self.caller_id:
            raise ValueError("execution identity is required")
        if self.duration_ms < 0 or self.attempt_count < 0:
            raise ValueError("execution duration and attempt count are invalid")
        if self.success and (not self.provider_id or not self.model_id or self.error_code):
            raise ValueError("successful execution requires provider/model and no error")
