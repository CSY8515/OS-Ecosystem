"""Health models shared by the runtime and components."""
from dataclasses import dataclass, field
from enum import Enum
from typing import Any

class HealthStatus(str, Enum):
    HEALTHY = "HEALTHY"
    DEGRADED = "DEGRADED"
    UNHEALTHY = "UNHEALTHY"
    DISABLED = "DISABLED"
    UNKNOWN = "UNKNOWN"

@dataclass(frozen=True, slots=True)
class HealthReport:
    """A component or capability health snapshot."""
    status: HealthStatus
    message: str = ""
    details: dict[str, Any] = field(default_factory=dict)
