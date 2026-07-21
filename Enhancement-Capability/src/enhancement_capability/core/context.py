"""Project-neutral request and execution context models."""
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any
from uuid import uuid4
from .errors import ContextValidationError

CAPABILITY_VERSION = "1.0.0"

def utc_now() -> datetime:
    return datetime.now(timezone.utc)

@dataclass(frozen=True, slots=True)
class EnhancementExecutionContext:
    source: str
    target: str
    action: str
    payload: dict[str, Any]
    request_id: str = field(default_factory=lambda: str(uuid4()))
    timestamp: datetime = field(default_factory=utc_now)
    capability_version: str = CAPABILITY_VERSION
    metadata: dict[str, Any] = field(default_factory=dict)

    def validate(self) -> None:
        for name in ("request_id", "source", "target", "action", "capability_version"):
            value = getattr(self, name)
            if not isinstance(value, str) or not value.strip():
                raise ContextValidationError(f"{name} must be a non-empty string")
        if not isinstance(self.payload, dict):
            raise ContextValidationError("payload must be a dictionary")
        if not isinstance(self.metadata, dict):
            raise ContextValidationError("metadata must be a dictionary")
        if not isinstance(self.timestamp, datetime) or self.timestamp.tzinfo is None:
            raise ContextValidationError("timestamp must be timezone-aware")
        if self.capability_version != CAPABILITY_VERSION:
            raise ContextValidationError(f"capability_version must be {CAPABILITY_VERSION}")

@dataclass(frozen=True, slots=True)
class EnhancementRequest:
    context: EnhancementExecutionContext
    component_id: str | None = None

    def validate(self) -> None:
        self.context.validate()
        if self.component_id is not None and (not isinstance(self.component_id, str) or not self.component_id.strip()):
            raise ContextValidationError("component_id must be a non-empty string when supplied")
