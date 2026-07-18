"""Minimal component used to verify the v1.0 runtime."""
from typing import Any
from safety_capability.core.context import SafetyExecutionContext
from safety_capability.core.errors import InputValidationError, OutputValidationError
from safety_capability.core.health import HealthReport, HealthStatus
from safety_capability.interfaces import SafetyComponent

class BasicValidationComponent(SafetyComponent):
    component_id = "basic-validation"
    component_name = "Basic Validation Component"
    version = "1.0.0"
    supported_actions = frozenset({"validate", "force_failure"})

    def validate_input(self, context: SafetyExecutionContext) -> None:
        if context.action not in self.supported_actions:
            raise InputValidationError(f"unsupported action: {context.action}")
        if context.action == "validate" and "value" not in context.payload:
            raise InputValidationError("payload must contain 'value'")

    def execute(self, context: SafetyExecutionContext) -> dict[str, Any]:
        if context.action == "force_failure":
            raise RuntimeError("intentional test failure")
        return {"valid": True, "validated_fields": sorted(context.payload), "value": context.payload["value"]}

    def validate_output(self, output: dict[str, Any], context: SafetyExecutionContext) -> None:
        if not isinstance(output, dict) or output.get("valid") is not True:
            raise OutputValidationError("output must report valid=true")

    def health_check(self) -> HealthReport:
        return HealthReport(HealthStatus.HEALTHY, "Basic validation component is ready")

    def metadata(self) -> dict[str, Any]:
        return {"purpose": "v1.0 runtime verification", "module_specific": False}
