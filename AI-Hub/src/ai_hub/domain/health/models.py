from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum


class HealthState(StrEnum):
    ONLINE = "Online"
    OFFLINE = "Offline"
    ERROR = "Error"
    UNKNOWN = "Unknown"
    DISABLED = "Disabled"


@dataclass(frozen=True, slots=True)
class HealthObservation:
    provider_id: str
    state: HealthState
    checked_at: datetime
    response_time_ms: float | None
    availability: float | None = None
    error_code: str | None = None
    source: str = "active"

    def __post_init__(self) -> None:
        if not self.provider_id.strip():
            raise ValueError("provider_id is required")
        if self.response_time_ms is not None and self.response_time_ms < 0:
            raise ValueError("response_time_ms cannot be negative")
        if self.availability is not None and not 0 <= self.availability <= 1:
            raise ValueError("availability must be between zero and one")
