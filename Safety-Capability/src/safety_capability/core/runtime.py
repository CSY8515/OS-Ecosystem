"""Safety Capability orchestration runtime."""
from time import perf_counter
from typing import Any
from safety_capability.database import ExecutionRepository, SQLiteExecutionRepository
from safety_capability.execution import SafetyExecutor
from safety_capability.registry import ComponentRegistry
from .context import CAPABILITY_VERSION, SafetyExecutionContext, SafetyRequest
from .errors import ErrorCode, SafetyCapabilityError
from .health import HealthReport, HealthStatus
from .result import SafetyResult

class SafetyRuntime:
    """Validate, route, execute, record, and return safety requests."""
    def __init__(self, *, registry: ComponentRegistry | None = None,
                 repository: ExecutionRepository | None = None,
                 executor: SafetyExecutor | None = None,
                 max_retries: int = 0) -> None:
        if max_retries < 0:
            raise ValueError("max_retries cannot be negative")
        self.registry = registry or ComponentRegistry()
        self.repository = repository or SQLiteExecutionRepository()
        self.executor = executor or SafetyExecutor()
        self.max_retries = max_retries

    def execute(self, request: SafetyRequest) -> SafetyResult:
        """Run a valid request without allowing execution failures to escape.

        A non-``SafetyRequest`` value or a request with a non-context payload is
        a caller programming error and raises ``TypeError`` before execution.
        """
        if not isinstance(request, SafetyRequest):
            raise TypeError("request must be a SafetyRequest")
        if not isinstance(request.context, SafetyExecutionContext):
            raise TypeError("request.context must be a SafetyExecutionContext")
        started = perf_counter()
        context = request.context
        component_id = request.component_id if isinstance(request.component_id, str) else ""
        retries = 0
        try:
            request.validate()
            if request.component_id:
                component = self.registry.get(request.component_id, require_enabled=True)
                if context.action not in component.supported_actions:
                    raise SafetyCapabilityError(
                        ErrorCode.ACTION_NOT_SUPPORTED,
                        f"component {component.component_id} does not support action: {context.action}",
                    )
            else:
                component = self.registry.find_for_action(context.action)
            component_id = component.component_id
            outcome = self.executor.execute(component, context)
            while (not outcome.success and outcome.error_code == ErrorCode.EXECUTION_FAILED
                   and retries < self.max_retries):
                retries += 1
                outcome = self.executor.execute(component, context)
            if outcome.success:
                result = self._result(True, context.request_id, component_id, context.action, "SUCCESS",
                                      None, "Safety execution completed", started, retries,
                                      CAPABILITY_VERSION, outcome.value or {})
            else:
                result = self._result(False, context.request_id, component_id, context.action, "FAILED",
                                      outcome.error_code, outcome.message, started, retries,
                                      CAPABILITY_VERSION, {})
        except SafetyCapabilityError as exc:
            result = self._result(False, context.request_id, component_id, context.action, "FAILED",
                                  exc.code, str(exc), started, retries, CAPABILITY_VERSION, {})
        except Exception as exc:
            result = self._result(False, context.request_id, component_id, context.action, "FAILED",
                                  ErrorCode.INTERNAL_ERROR, f"internal runtime error: {exc}", started,
                                  retries, CAPABILITY_VERSION, {})
        try:
            self.repository.save(result, source=context.source, target=context.target)
        except Exception as exc:
            return self._result(False, context.request_id, component_id, context.action, "FAILED",
                                ErrorCode.REPOSITORY_ERROR, f"execution record could not be saved: {exc}",
                                started, retries, CAPABILITY_VERSION,
                                {"original_result": result.to_dict()})
        return result

    def _result(self, success: bool, request_id: str, component_id: str, action: str,
                status: str, error_code: ErrorCode | None, message: str, started: float,
                retry_count: int, version: str, details: dict[str, Any]) -> SafetyResult:
        return SafetyResult(success, request_id, component_id, action, status,
                            error_code.value if error_code else None, message,
                            perf_counter() - started, retry_count, None, version, details=details)

    def health_check(self) -> dict[str, object]:
        """Return capability health separately from component reports."""
        components = self.registry.health()
        statuses = {report.status for report in components.values()}
        if not components:
            capability = HealthReport(HealthStatus.UNKNOWN, "No components registered")
        elif statuses <= {HealthStatus.HEALTHY, HealthStatus.DISABLED} and HealthStatus.HEALTHY in statuses:
            capability = HealthReport(HealthStatus.HEALTHY, "Runtime and enabled components are healthy")
        elif HealthStatus.HEALTHY in statuses or HealthStatus.DEGRADED in statuses:
            capability = HealthReport(HealthStatus.DEGRADED, "One or more components need attention")
        else:
            capability = HealthReport(HealthStatus.UNHEALTHY, "No healthy enabled component")
        return {"capability": capability, "components": components}

    def close(self) -> None:
        self.repository.close()

    def __enter__(self) -> "SafetyRuntime":
        return self

    def __exit__(self, *_: object) -> None:
        self.close()
