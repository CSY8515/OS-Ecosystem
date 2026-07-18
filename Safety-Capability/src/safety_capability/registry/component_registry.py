"""Thread-safe component registry."""
from dataclasses import dataclass
from threading import RLock
from safety_capability.core.errors import ErrorCode, SafetyCapabilityError
from safety_capability.core.health import HealthReport, HealthStatus
from safety_capability.interfaces import SafetyComponent

@dataclass(slots=True)
class ComponentRegistration:
    component: SafetyComponent
    enabled: bool = True

class ComponentRegistry:
    """Registers, discovers, enables, and checks components."""
    def __init__(self) -> None:
        self._items: dict[str, ComponentRegistration] = {}
        self._lock = RLock()

    def register(self, component: SafetyComponent, *, enabled: bool = True) -> None:
        component_id = getattr(component, "component_id", "")
        if not isinstance(component_id, str) or not component_id.strip():
            raise ValueError("component_id must be a non-empty string")
        if not getattr(component, "supported_actions", frozenset()):
            raise ValueError("component must support at least one action")
        with self._lock:
            if component_id in self._items:
                raise ValueError(f"component already registered: {component_id}")
            self._items[component_id] = ComponentRegistration(component, enabled)

    def get(self, component_id: str, *, require_enabled: bool = False) -> SafetyComponent:
        with self._lock:
            registration = self._items.get(component_id)
            if registration is None:
                raise SafetyCapabilityError(ErrorCode.COMPONENT_NOT_FOUND, f"component not found: {component_id}")
            if require_enabled and not registration.enabled:
                raise SafetyCapabilityError(ErrorCode.COMPONENT_DISABLED, f"component is disabled: {component_id}")
            return registration.component

    def find_for_action(self, action: str) -> SafetyComponent:
        with self._lock:
            candidates = sorted(
                (item.component for item in self._items.values() if item.enabled and action in item.component.supported_actions),
                key=lambda component: component.component_id,
            )
        if not candidates:
            raise SafetyCapabilityError(ErrorCode.ACTION_NOT_SUPPORTED, f"no enabled component supports action: {action}")
        return candidates[0]

    def set_enabled(self, component_id: str, enabled: bool) -> None:
        self.get(component_id)
        with self._lock:
            self._items[component_id].enabled = enabled

    def is_enabled(self, component_id: str) -> bool:
        self.get(component_id)
        with self._lock:
            return self._items[component_id].enabled

    def list_components(self) -> list[dict[str, object]]:
        with self._lock:
            return [
                {"component_id": item.component.component_id, "component_name": item.component.component_name,
                 "version": item.component.version, "supported_actions": sorted(item.component.supported_actions),
                 "enabled": item.enabled}
                for item in sorted(self._items.values(), key=lambda value: value.component.component_id)
            ]

    def health(self) -> dict[str, HealthReport]:
        reports: dict[str, HealthReport] = {}
        with self._lock:
            items = list(self._items.items())
        for component_id, item in items:
            if not item.enabled:
                reports[component_id] = HealthReport(HealthStatus.DISABLED, "Component is disabled")
                continue
            try:
                report = item.component.health_check()
                if not isinstance(report, HealthReport):
                    raise TypeError("health_check must return HealthReport")
                reports[component_id] = report
            except Exception as exc:  # isolation is intentional at the registry boundary
                reports[component_id] = HealthReport(HealthStatus.UNKNOWN, f"Health check failed: {exc}")
        return reports
