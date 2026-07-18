"""Stable Safety Capability result schema."""
from dataclasses import asdict, dataclass, field
from datetime import datetime
from typing import Any
from .context import utc_now

@dataclass(frozen=True, slots=True)
class SafetyResult:
    """Common response returned and persisted for every execution."""
    success: bool
    request_id: str
    component_id: str
    action: str
    status: str
    error_code: str | None
    message: str
    execution_time: float
    retry_count: int
    recovery_result: dict[str, Any] | None
    capability_version: str
    timestamp: datetime = field(default_factory=utc_now)
    details: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """Convert the result to a JSON-friendly mapping."""
        data = asdict(self)
        data["timestamp"] = self.timestamp.isoformat()
        return data
