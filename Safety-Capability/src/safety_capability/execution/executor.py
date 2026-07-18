"""Validation and execution boundary for one component."""
from safety_capability.core.context import SafetyExecutionContext
from safety_capability.core.errors import InputValidationError, OutputValidationError
from safety_capability.interfaces import SafetyComponent
from .failure_isolation import FailureIsolation, IsolationOutcome

class SafetyExecutor:
    """Executes a component behind a failure-isolation boundary."""
    def __init__(self, isolation: FailureIsolation | None = None) -> None:
        self._isolation = isolation or FailureIsolation()

    def execute(self, component: SafetyComponent, context: SafetyExecutionContext) -> IsolationOutcome:
        def operation() -> dict[str, object]:
            try:
                component.validate_input(context)
            except InputValidationError:
                raise
            except Exception as exc:
                raise InputValidationError(str(exc)) from exc
            output = component.execute(context)
            try:
                component.validate_output(output, context)
            except OutputValidationError:
                raise
            except Exception as exc:
                raise OutputValidationError(str(exc)) from exc
            return output
        return self._isolation.run(operation)
