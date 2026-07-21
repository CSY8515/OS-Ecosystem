"""Public request and result contracts for Personal Secretary."""
from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any
from uuid import uuid4

CAPABILITY_VERSION = "1.0.0"


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


@dataclass(frozen=True, slots=True)
class SecretaryContext:
    source: str
    action: str
    payload: dict[str, Any]
    target: str = "personal-secretary"
    metadata: dict[str, Any] = field(default_factory=dict)
    request_id: str = field(default_factory=lambda: str(uuid4()))
    timestamp: datetime = field(default_factory=utc_now)

    def validate(self) -> None:
        if not self.source.strip() or not self.action.strip():
            raise ValueError("source and action are required")
        if not isinstance(self.payload, dict):
            raise TypeError("payload must be a dictionary")


@dataclass(frozen=True, slots=True)
class SecretaryRequest:
    context: SecretaryContext


@dataclass(frozen=True, slots=True)
class SecretaryResult:
    success: bool
    request_id: str
    action: str
    status: str
    message: str
    details: dict[str, Any]
    error_code: str | None = None
    capability_version: str = CAPABILITY_VERSION
    timestamp: datetime = field(default_factory=utc_now)

    def to_dict(self) -> dict[str, Any]:
        item = asdict(self)
        item["timestamp"] = self.timestamp.isoformat()
        return item
