"""Automation Capability v1.0 public API and governed runtime."""

from __future__ import annotations

import json
import sqlite3
from dataclasses import asdict, dataclass, field, replace
from datetime import datetime, timedelta
from pathlib import Path
from threading import RLock
from time import perf_counter
from typing import Any, Protocol

from .core.context import CAPABILITY_VERSION, AutomationExecutionContext, AutomationRequest, utc_now
from .core.errors import AutomationCapabilityError, ErrorCode, InputValidationError, OutputValidationError

__version__ = CAPABILITY_VERSION


@dataclass(frozen=True, slots=True)
class SafetyDecision:
    allowed: bool = True
    risk_level: str = "LOW"
    approval_required: bool = False
    reason: str = "Safety checks passed"


class SafetyGateway(Protocol):
    def assess(self, context: AutomationExecutionContext) -> SafetyDecision: ...
    def recover(self, context: AutomationExecutionContext, error: Exception) -> dict[str, Any]: ...


class DefaultSafetyGateway:
    """Replaceable adapter for the independent Safety Capability."""

    def assess(self, context: AutomationExecutionContext) -> SafetyDecision:
        risk = str(context.metadata.get("risk_level", "LOW")).upper()
        if risk not in {"LOW", "MEDIUM", "HIGH", "CRITICAL"}:
            raise InputValidationError("risk_level must be LOW, MEDIUM, HIGH, or CRITICAL")
        if risk == "CRITICAL":
            return SafetyDecision(False, risk, True, "Critical-risk automation is blocked")
        return SafetyDecision(True, risk, context.action == "auto_execute" or risk == "HIGH")

    def recover(self, context: AutomationExecutionContext, error: Exception) -> dict[str, Any]:
        return {"available": True, "strategy": "safe-stop", "request_id": context.request_id}


class EnhancementGateway(Protocol):
    def insights(self, context: AutomationExecutionContext) -> dict[str, Any]: ...


class NullEnhancementGateway:
    def insights(self, context: AutomationExecutionContext) -> dict[str, Any]:
        return {}


class StaticEnhancementGateway:
    def __init__(self, insights: dict[str, Any]) -> None:
        self._insights = dict(insights)

    def insights(self, context: AutomationExecutionContext) -> dict[str, Any]:
        return dict(self._insights)


@dataclass(frozen=True, slots=True)
class AutomationResult:
    success: bool
    request_id: str
    component_id: str
    action: str
    status: str
    error_code: str | None
    message: str
    execution_time: float
    capability_version: str
    stages: tuple[str, ...]
    timestamp: datetime = field(default_factory=utc_now)
    details: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        item = asdict(self)
        item["timestamp"], item["stages"] = self.timestamp.isoformat(), list(self.stages)
        return item


class HealthStatus(str):
    HEALTHY, DISABLED, UNKNOWN = "HEALTHY", "DISABLED", "UNKNOWN"


@dataclass(frozen=True, slots=True)
class HealthReport:
    status: str
    message: str = ""


class AutomationComponent:
    component_id: str
    component_name: str
    version = CAPABILITY_VERSION
    supported_actions: frozenset[str]
    required_fields: tuple[str, ...] = ()

    def validate_input(self, context: AutomationExecutionContext) -> None:
        if context.action not in self.supported_actions:
            raise InputValidationError(f"unsupported action: {context.action}")
        missing = [name for name in self.required_fields if name not in context.payload]
        if missing:
            raise InputValidationError(f"payload must contain: {', '.join(missing)}")

    def execute(self, context: AutomationExecutionContext) -> dict[str, Any]:
        raise NotImplementedError

    def validate_output(self, output: dict[str, Any], context: AutomationExecutionContext) -> None:
        if not isinstance(output, dict) or output.get("module") != self.component_id:
            raise OutputValidationError("output must identify the executing module")

    def health_check(self) -> HealthReport:
        return HealthReport(HealthStatus.HEALTHY, f"{self.component_name} is ready")


class WorkflowComponent(AutomationComponent):
    component_id, component_name = "workflow", "Workflow"
    supported_actions, required_fields = frozenset({"manage_workflow"}), ("steps",)

    def execute(self, context: AutomationExecutionContext) -> dict[str, Any]:
        steps = context.payload["steps"]
        if not isinstance(steps, list) or not steps:
            raise InputValidationError("steps must be a non-empty list")
        normalized = []
        for index, step in enumerate(steps, start=1):
            if not isinstance(step, dict) or not str(step.get("name", "")).strip():
                raise InputValidationError("each step must contain a name")
            normalized.append({"order": index, "name": str(step["name"]), "depends_on": list(step.get("depends_on", []))})
        return {"module": self.component_id, "workflow_id": str(context.payload.get("workflow_id", context.request_id)), "step_count": len(normalized), "steps": normalized}


class SchedulerComponent(AutomationComponent):
    component_id, component_name = "scheduler", "Scheduler"
    supported_actions, required_fields = frozenset({"schedule"}), ("schedule_type",)

    def execute(self, context: AutomationExecutionContext) -> dict[str, Any]:
        kind = context.payload["schedule_type"]
        if kind == "once":
            run_at = context.payload.get("run_at")
            if not isinstance(run_at, str) or not run_at.strip():
                raise InputValidationError("once schedules require run_at")
            next_run, recurring = run_at, False
        elif kind == "interval":
            minutes = context.payload.get("interval_minutes")
            if not isinstance(minutes, int) or isinstance(minutes, bool) or minutes < 1:
                raise InputValidationError("interval schedules require a positive interval_minutes")
            next_run, recurring = (context.timestamp + timedelta(minutes=minutes)).isoformat(), True
        else:
            raise InputValidationError("schedule_type must be once or interval")
        return {"module": self.component_id, "schedule_type": kind, "next_run": next_run, "recurring": recurring}


class TriggerComponent(AutomationComponent):
    component_id, component_name = "trigger", "Trigger"
    supported_actions, required_fields = frozenset({"evaluate_trigger"}), ("condition", "event")

    def execute(self, context: AutomationExecutionContext) -> dict[str, Any]:
        condition, event = context.payload["condition"], context.payload["event"]
        if not isinstance(condition, dict) or not isinstance(event, dict):
            raise InputValidationError("condition and event must be dictionaries")
        field, operator, expected = condition.get("field"), condition.get("operator", "equals"), condition.get("value")
        if not isinstance(field, str) or field not in event:
            raise InputValidationError("condition field must exist in event")
        actual = event[field]
        operations = {"equals": lambda: actual == expected, "not_equals": lambda: actual != expected, "greater_than": lambda: actual > expected, "contains": lambda: expected in actual}
        if operator not in operations:
            raise InputValidationError("unsupported trigger operator")
        try:
            matched = bool(operations[operator]())
        except (TypeError, ValueError) as exc:
            raise InputValidationError("condition values are not comparable") from exc
        return {"module": self.component_id, "matched": matched, "field": field, "operator": operator}


class RoutineComponent(AutomationComponent):
    component_id, component_name = "routine", "Routine"
    supported_actions, required_fields = frozenset({"manage_routine"}), ("cadence", "tasks")

    def execute(self, context: AutomationExecutionContext) -> dict[str, Any]:
        cadence, tasks = context.payload["cadence"], context.payload["tasks"]
        days = {"daily": 1, "weekly": 7, "monthly": 30}
        if cadence not in days:
            raise InputValidationError("cadence must be daily, weekly, or monthly")
        if not isinstance(tasks, list) or not tasks or not all(isinstance(task, str) and task.strip() for task in tasks):
            raise InputValidationError("tasks must be a non-empty string list")
        return {"module": self.component_id, "cadence": cadence, "task_count": len(tasks), "tasks": tasks, "next_cycle": (context.timestamp + timedelta(days=days[cadence])).isoformat()}


class AutoExecutionComponent(AutomationComponent):
    component_id, component_name = "auto-execution", "Auto Execution"
    supported_actions, required_fields = frozenset({"auto_execute"}), ("task", "approval")

    def execute(self, context: AutomationExecutionContext) -> dict[str, Any]:
        task = context.payload["task"]
        if not isinstance(task, dict) or not str(task.get("name", "")).strip():
            raise InputValidationError("task must contain a name")
        return {"module": self.component_id, "execution_id": f"exec-{context.request_id}", "task": task["name"], "status": "EXECUTED", "logged": True, "recovery": "AVAILABLE"}


class AutoDecisionComponent(AutomationComponent):
    component_id, component_name = "auto-decision", "Auto Decision"
    supported_actions, required_fields = frozenset({"auto_decide"}), ("candidates",)

    def execute(self, context: AutomationExecutionContext) -> dict[str, Any]:
        candidates = context.payload["candidates"]
        if not isinstance(candidates, list) or not candidates:
            raise InputValidationError("candidates must be a non-empty list")
        try:
            recommended = max(candidates, key=lambda item: item["score"])
        except (KeyError, TypeError) as exc:
            raise InputValidationError("each candidate must contain a comparable score") from exc
        policy = context.payload.get("approval_policy", "manual")
        if policy not in {"manual", "threshold", "automatic"}:
            raise InputValidationError("approval_policy must be manual, threshold, or automatic")
        threshold = context.payload.get("approval_threshold", 1.0)
        approval_required = policy == "manual" or (policy == "threshold" and recommended["score"] < threshold)
        return {"module": self.component_id, "candidate_count": len(candidates), "recommended": recommended, "approval_policy": policy, "approval_required": approval_required, "enhancement_inputs": dict(context.metadata.get("enhancement_inputs", {}))}


class ComponentRegistry:
    def __init__(self) -> None:
        self._items: dict[str, tuple[AutomationComponent, bool]] = {}
        self._lock = RLock()

    def register(self, component: AutomationComponent, *, enabled: bool = True) -> None:
        with self._lock:
            if component.component_id in self._items:
                raise ValueError(f"component already registered: {component.component_id}")
            self._items[component.component_id] = (component, enabled)

    def get(self, component_id: str, *, require_enabled: bool = False) -> AutomationComponent:
        item = self._items.get(component_id)
        if item is None:
            raise AutomationCapabilityError(ErrorCode.COMPONENT_NOT_FOUND, f"component not found: {component_id}")
        if require_enabled and not item[1]:
            raise AutomationCapabilityError(ErrorCode.COMPONENT_DISABLED, f"component is disabled: {component_id}")
        return item[0]

    def find_for_action(self, action: str) -> AutomationComponent:
        matches = sorted((component for component, enabled in self._items.values() if enabled and action in component.supported_actions), key=lambda component: component.component_id)
        if not matches:
            raise AutomationCapabilityError(ErrorCode.ACTION_NOT_SUPPORTED, f"no enabled component supports action: {action}")
        return matches[0]

    def set_enabled(self, component_id: str, enabled: bool) -> None:
        component = self.get(component_id)
        self._items[component_id] = (component, enabled)

    def list_components(self) -> list[dict[str, object]]:
        return [{"component_id": component.component_id, "component_name": component.component_name, "version": component.version, "supported_actions": sorted(component.supported_actions), "enabled": enabled} for component, enabled in sorted(self._items.values(), key=lambda item: item[0].component_id)]

    def health(self) -> dict[str, HealthReport]:
        return {component.component_id: component.health_check() if enabled else HealthReport(HealthStatus.DISABLED, "Component is disabled") for component, enabled in self._items.values()}


class SQLiteExecutionRepository:
    def __init__(self, database_path: str | Path = ":memory:") -> None:
        self.database_path = str(database_path)
        if self.database_path != ":memory:":
            Path(self.database_path).parent.mkdir(parents=True, exist_ok=True)
        self._connection = sqlite3.connect(self.database_path)
        self._connection.row_factory = sqlite3.Row
        self._connection.execute("CREATE TABLE IF NOT EXISTS executions (request_id TEXT PRIMARY KEY, success INTEGER, component_id TEXT, action TEXT, status TEXT, error_code TEXT, message TEXT, execution_time REAL, capability_version TEXT, stages TEXT, timestamp TEXT, details TEXT, source TEXT, target TEXT)")

    def save(self, result: AutomationResult, *, source: str, target: str) -> None:
        item = result.to_dict()
        with self._connection:
            self._connection.execute("INSERT INTO executions VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (item["request_id"], int(item["success"]), item["component_id"], item["action"], item["status"], item["error_code"], item["message"], item["execution_time"], item["capability_version"], json.dumps(item["stages"]), item["timestamp"], json.dumps(item["details"]), source, target))

    def get(self, request_id: str) -> dict[str, Any] | None:
        row = self._connection.execute("SELECT * FROM executions WHERE request_id = ?", (request_id,)).fetchone()
        if row is None:
            return None
        item = dict(row)
        item["success"] = bool(item["success"])
        item["stages"], item["details"] = json.loads(item["stages"]), json.loads(item["details"])
        return item

    def count(self) -> int:
        return int(self._connection.execute("SELECT COUNT(*) FROM executions").fetchone()[0])

    def close(self) -> None:
        self._connection.close()


class AutomationRuntime:
    def __init__(self, *, registry: ComponentRegistry | None = None, repository: SQLiteExecutionRepository | None = None, safety_gateway: SafetyGateway | None = None, enhancement_gateway: EnhancementGateway | None = None) -> None:
        self.registry = registry or ComponentRegistry()
        self.repository = repository or SQLiteExecutionRepository()
        self.safety_gateway = safety_gateway or DefaultSafetyGateway()
        self.enhancement_gateway = enhancement_gateway or NullEnhancementGateway()

    def execute(self, request: AutomationRequest) -> AutomationResult:
        if not isinstance(request, AutomationRequest):
            raise TypeError("request must be an AutomationRequest")
        if not isinstance(request.context, AutomationExecutionContext):
            raise TypeError("request.context must be an AutomationExecutionContext")
        started, context, component_id = perf_counter(), request.context, request.component_id or ""
        stages: list[str] = []
        try:
            request.validate()
            stages.append("Validation")
            component = self.registry.get(request.component_id, require_enabled=True) if request.component_id else self.registry.find_for_action(context.action)
            component_id = component.component_id
            component.validate_input(context)
            safety = self.safety_gateway.assess(context)
            stages.append("Risk Check")
            if not safety.allowed:
                raise AutomationCapabilityError(ErrorCode.SAFETY_REJECTED, safety.reason)
            approval = context.payload.get("approval", {})
            approved = isinstance(approval, dict) and approval.get("approved") is True
            stages.append("Approval")
            if safety.approval_required and not approved:
                raise AutomationCapabilityError(ErrorCode.APPROVAL_REQUIRED, "Explicit user approval is required")
            insights = self.enhancement_gateway.insights(context)
            if not isinstance(insights, dict):
                raise InputValidationError("enhancement insights must be a dictionary")
            enriched = replace(context, metadata={**context.metadata, "enhancement_inputs": insights})
            details = component.execute(enriched)
            stages.append("Execution")
            component.validate_output(details, enriched)
            stages.append("Logging")
            result = AutomationResult(True, context.request_id, component_id, context.action, "SUCCESS", None, "Automation execution completed", perf_counter() - started, CAPABILITY_VERSION, tuple(stages), details=details)
        except AutomationCapabilityError as exc:
            status = "PENDING_APPROVAL" if exc.code == ErrorCode.APPROVAL_REQUIRED else "BLOCKED" if exc.code == ErrorCode.SAFETY_REJECTED else "FAILED"
            stages.append("Logging")
            result = AutomationResult(False, context.request_id, component_id, context.action, status, exc.code.value, str(exc), perf_counter() - started, CAPABILITY_VERSION, tuple(stages))
        except Exception as exc:
            recovery = self.safety_gateway.recover(context, exc)
            stages.extend(("Recovery", "Logging"))
            result = AutomationResult(False, context.request_id, component_id, context.action, "FAILED", ErrorCode.EXECUTION_FAILED.value, f"component execution failed: {exc}", perf_counter() - started, CAPABILITY_VERSION, tuple(stages), details={"recovery": recovery})
        self.repository.save(result, source=context.source, target=context.target)
        return result

    def health_check(self) -> dict[str, object]:
        components = self.registry.health()
        healthy = any(report.status == HealthStatus.HEALTHY for report in components.values())
        return {"capability": HealthReport(HealthStatus.HEALTHY if healthy else HealthStatus.UNKNOWN, "Runtime health derived from registered modules"), "components": components}

    def close(self) -> None:
        self.repository.close()

    def __enter__(self) -> "AutomationRuntime":
        return self

    def __exit__(self, *_: object) -> None:
        self.close()


BUILTIN_COMPONENTS = (WorkflowComponent, SchedulerComponent, TriggerComponent, RoutineComponent, AutoExecutionComponent, AutoDecisionComponent)


def create_default_runtime(*, repository: SQLiteExecutionRepository | None = None, safety_gateway: SafetyGateway | None = None, enhancement_gateway: EnhancementGateway | None = None) -> AutomationRuntime:
    runtime = AutomationRuntime(repository=repository, safety_gateway=safety_gateway, enhancement_gateway=enhancement_gateway)
    for component_type in BUILTIN_COMPONENTS:
        runtime.registry.register(component_type())
    return runtime


__all__ = [
    "CAPABILITY_VERSION", "AutomationExecutionContext", "AutomationRequest", "AutomationResult",
    "AutomationRuntime", "ComponentRegistry", "SQLiteExecutionRepository", "SafetyDecision",
    "SafetyGateway", "DefaultSafetyGateway", "EnhancementGateway", "NullEnhancementGateway",
    "StaticEnhancementGateway", "HealthReport", "HealthStatus", "create_default_runtime",
]
