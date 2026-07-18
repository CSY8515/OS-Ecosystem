"""Exception isolation for component calls."""
from dataclasses import dataclass
from typing import Any, Callable
from safety_capability.core.errors import ErrorCode, SafetyCapabilityError

@dataclass(frozen=True, slots=True)
class IsolationOutcome:
    success: bool
    value: dict[str, Any] | None = None
    error_code: ErrorCode | None = None
    message: str = ""

class FailureIsolation:
    """Converts component exceptions into controlled outcomes."""
    def run(self, operation: Callable[[], dict[str, Any]]) -> IsolationOutcome:
        try:
            return IsolationOutcome(True, value=operation())
        except SafetyCapabilityError as exc:
            return IsolationOutcome(False, error_code=exc.code, message=str(exc))
        except Exception as exc:
            return IsolationOutcome(False, error_code=ErrorCode.EXECUTION_FAILED,
                                    message=f"component execution failed: {exc}")
