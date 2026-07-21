"""Enhancement Capability v1.0 public API and independent runtime."""
from collections import Counter
from dataclasses import asdict, dataclass, field
from datetime import datetime
import json
import sqlite3
from pathlib import Path
from threading import RLock
from time import perf_counter
from typing import Any

from .core.context import CAPABILITY_VERSION, EnhancementExecutionContext, EnhancementRequest, utc_now
from .core.errors import EnhancementCapabilityError, ErrorCode, InputValidationError, OutputValidationError

__version__ = CAPABILITY_VERSION

@dataclass(frozen=True, slots=True)
class EnhancementResult:
    success: bool
    request_id: str
    component_id: str
    action: str
    status: str
    error_code: str | None
    message: str
    execution_time: float
    capability_version: str
    timestamp: datetime = field(default_factory=utc_now)
    details: dict[str, Any] = field(default_factory=dict)
    def to_dict(self) -> dict[str, Any]:
        item = asdict(self)
        item["timestamp"] = self.timestamp.isoformat()
        return item

class HealthStatus(str):
    HEALTHY, DISABLED, UNKNOWN = "HEALTHY", "DISABLED", "UNKNOWN"

@dataclass(frozen=True, slots=True)
class HealthReport:
    status: str
    message: str = ""

class EnhancementComponent:
    component_id: str
    component_name: str
    version = CAPABILITY_VERSION
    supported_actions: frozenset[str]
    required_field: str
    def validate_input(self, context: EnhancementExecutionContext) -> None:
        if context.action not in self.supported_actions:
            raise InputValidationError(f"unsupported action: {context.action}")
        if self.required_field not in context.payload:
            raise InputValidationError(f"payload must contain '{self.required_field}'")
    def execute(self, context: EnhancementExecutionContext) -> dict[str, Any]:
        raise NotImplementedError
    def validate_output(self, output: dict[str, Any], context: EnhancementExecutionContext) -> None:
        if not isinstance(output, dict) or output.get("module") != self.component_id:
            raise OutputValidationError("output must identify the executing module")
    def health_check(self) -> HealthReport:
        return HealthReport(HealthStatus.HEALTHY, f"{self.component_name} is ready")
    def metadata(self) -> dict[str, Any]:
        return {"scope": "project-neutral", "capability": "enhancement"}

class AnalyticsComponent(EnhancementComponent):
    component_id, component_name = "analytics", "Analytics"
    supported_actions, required_field = frozenset({"analyze"}), "values"
    def validate_input(self, context: EnhancementExecutionContext) -> None:
        super().validate_input(context)
        values = context.payload["values"]
        if not isinstance(values, list) or not values or any(isinstance(value, bool) or not isinstance(value, (int, float)) for value in values):
            raise InputValidationError("values must be a non-empty numeric list")
    def execute(self, context: EnhancementExecutionContext) -> dict[str, Any]:
        values = context.payload["values"]
        return {"module": self.component_id, "count": len(values), "total": sum(values), "mean": sum(values) / len(values), "minimum": min(values), "maximum": max(values)}

class LearningComponent(EnhancementComponent):
    component_id, component_name = "learning", "Learning"
    supported_actions, required_field = frozenset({"learn"}), "examples"
    def execute(self, context: EnhancementExecutionContext) -> dict[str, Any]:
        examples = context.payload["examples"]
        if not isinstance(examples, list):
            raise InputValidationError("examples must be a list")
        return {"module": self.component_id, "learned_count": len(examples), "knowledge_keys": sorted({key for item in examples if isinstance(item, dict) for key in item})}

class PatternAnalysisComponent(EnhancementComponent):
    component_id, component_name = "pattern-analysis", "Pattern Analysis"
    supported_actions, required_field = frozenset({"analyze_patterns"}), "items"
    def execute(self, context: EnhancementExecutionContext) -> dict[str, Any]:
        items = context.payload["items"]
        if not isinstance(items, list):
            raise InputValidationError("items must be a list")
        counts = Counter(str(item) for item in items)
        return {"module": self.component_id, "frequencies": dict(sorted(counts.items())), "repeated": sorted(key for key, count in counts.items() if count > 1)}

class KnowledgeManagementComponent(EnhancementComponent):
    component_id, component_name = "knowledge-management", "Knowledge Management"
    supported_actions, required_field = frozenset({"manage_knowledge"}), "entries"
    def execute(self, context: EnhancementExecutionContext) -> dict[str, Any]:
        entries = context.payload["entries"]
        if not isinstance(entries, dict):
            raise InputValidationError("entries must be a dictionary")
        return {"module": self.component_id, "entry_count": len(entries), "entries": dict(sorted(entries.items()))}

class OptimizationComponent(EnhancementComponent):
    component_id, component_name = "optimization", "Optimization"
    supported_actions, required_field = frozenset({"optimize"}), "candidates"
    def execute(self, context: EnhancementExecutionContext) -> dict[str, Any]:
        candidates = context.payload["candidates"]
        if not isinstance(candidates, list) or not candidates:
            raise InputValidationError("candidates must be a non-empty list")
        try:
            best = max(candidates, key=lambda item: item["score"])
        except (KeyError, TypeError) as exc:
            raise InputValidationError("each candidate must contain a comparable score") from exc
        return {"module": self.component_id, "evaluated_count": len(candidates), "best": best}

class RuleGenerationComponent(EnhancementComponent):
    component_id, component_name = "rule-generation", "Rule Generation"
    supported_actions, required_field = frozenset({"generate_rules"}), "patterns"
    def execute(self, context: EnhancementExecutionContext) -> dict[str, Any]:
        patterns = context.payload["patterns"]
        if not isinstance(patterns, list):
            raise InputValidationError("patterns must be a list")
        rules = [{"id": f"rule-{index:03d}", "condition": str(pattern), "enabled": True} for index, pattern in enumerate(dict.fromkeys(patterns), start=1)]
        return {"module": self.component_id, "rule_count": len(rules), "rules": rules}

class ComponentRegistry:
    def __init__(self) -> None:
        self._items: dict[str, tuple[EnhancementComponent, bool]] = {}
        self._lock = RLock()
    def register(self, component: EnhancementComponent, *, enabled: bool = True) -> None:
        with self._lock:
            if component.component_id in self._items:
                raise ValueError(f"component already registered: {component.component_id}")
            self._items[component.component_id] = (component, enabled)
    def get(self, component_id: str, *, require_enabled: bool = False) -> EnhancementComponent:
        item = self._items.get(component_id)
        if item is None:
            raise EnhancementCapabilityError(ErrorCode.COMPONENT_NOT_FOUND, f"component not found: {component_id}")
        if require_enabled and not item[1]:
            raise EnhancementCapabilityError(ErrorCode.COMPONENT_DISABLED, f"component is disabled: {component_id}")
        return item[0]
    def find_for_action(self, action: str) -> EnhancementComponent:
        matches = sorted((component for component, enabled in self._items.values() if enabled and action in component.supported_actions), key=lambda component: component.component_id)
        if not matches:
            raise EnhancementCapabilityError(ErrorCode.ACTION_NOT_SUPPORTED, f"no enabled component supports action: {action}")
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
        self._connection.execute("CREATE TABLE IF NOT EXISTS executions (request_id TEXT PRIMARY KEY, success INTEGER, component_id TEXT, action TEXT, status TEXT, error_code TEXT, message TEXT, execution_time REAL, capability_version TEXT, timestamp TEXT, details TEXT, source TEXT, target TEXT)")
    def save(self, result: EnhancementResult, *, source: str, target: str) -> None:
        item = result.to_dict()
        with self._connection:
            self._connection.execute("INSERT INTO executions VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (item["request_id"], int(item["success"]), item["component_id"], item["action"], item["status"], item["error_code"], item["message"], item["execution_time"], item["capability_version"], item["timestamp"], json.dumps(item["details"]), source, target))
    def get(self, request_id: str) -> dict[str, Any] | None:
        row = self._connection.execute("SELECT * FROM executions WHERE request_id = ?", (request_id,)).fetchone()
        if row is None: return None
        item = dict(row); item["success"] = bool(item["success"]); item["details"] = json.loads(item["details"]); return item
    def count(self) -> int:
        return int(self._connection.execute("SELECT COUNT(*) FROM executions").fetchone()[0])
    def close(self) -> None:
        self._connection.close()

class EnhancementRuntime:
    def __init__(self, *, registry: ComponentRegistry | None = None, repository: SQLiteExecutionRepository | None = None) -> None:
        self.registry, self.repository = registry or ComponentRegistry(), repository or SQLiteExecutionRepository()
    def execute(self, request: EnhancementRequest) -> EnhancementResult:
        if not isinstance(request, EnhancementRequest): raise TypeError("request must be an EnhancementRequest")
        if not isinstance(request.context, EnhancementExecutionContext): raise TypeError("request.context must be an EnhancementExecutionContext")
        started, context, component_id = perf_counter(), request.context, request.component_id or ""
        try:
            request.validate()
            component = self.registry.get(request.component_id, require_enabled=True) if request.component_id else self.registry.find_for_action(context.action)
            component_id = component.component_id
            component.validate_input(context); details = component.execute(context); component.validate_output(details, context)
            result = EnhancementResult(True, context.request_id, component_id, context.action, "SUCCESS", None, "Enhancement execution completed", perf_counter() - started, CAPABILITY_VERSION, details=details)
        except EnhancementCapabilityError as exc:
            result = EnhancementResult(False, context.request_id, component_id, context.action, "FAILED", exc.code.value, str(exc), perf_counter() - started, CAPABILITY_VERSION)
        except Exception as exc:
            result = EnhancementResult(False, context.request_id, component_id, context.action, "FAILED", ErrorCode.EXECUTION_FAILED.value, f"component execution failed: {exc}", perf_counter() - started, CAPABILITY_VERSION)
        self.repository.save(result, source=context.source, target=context.target)
        return result
    def health_check(self) -> dict[str, object]:
        components = self.registry.health()
        healthy = any(report.status == HealthStatus.HEALTHY for report in components.values())
        return {"capability": HealthReport(HealthStatus.HEALTHY if healthy else HealthStatus.UNKNOWN, "Runtime health derived from registered modules"), "components": components}
    def close(self) -> None: self.repository.close()
    def __enter__(self) -> "EnhancementRuntime": return self
    def __exit__(self, *_: object) -> None: self.close()

BUILTIN_COMPONENTS = (AnalyticsComponent, LearningComponent, PatternAnalysisComponent, KnowledgeManagementComponent, OptimizationComponent, RuleGenerationComponent)
def create_default_runtime(*, repository: SQLiteExecutionRepository | None = None) -> EnhancementRuntime:
    runtime = EnhancementRuntime(repository=repository)
    for component_type in BUILTIN_COMPONENTS: runtime.registry.register(component_type())
    return runtime
