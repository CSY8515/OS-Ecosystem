from safety_capability import (
    BasicValidationComponent,
    ComponentRegistry,
    ExecutionRepository,
    SafetyExecutionContext,
    SafetyRequest,
    SafetyRuntime,
)
from safety_capability import __version__


class InvalidOutputComponent(BasicValidationComponent):
    component_id = "invalid-output"

    def execute(self, context):
        return {"valid": False}


class BrokenRepository(ExecutionRepository):
    def save(self, result, *, source, target):
        raise OSError("simulated repository outage")

    def get(self, request_id):
        return None

    def list_records(self, limit=100):
        return []

    def count(self):
        return 0

    def close(self):
        pass


def test_public_version_and_recovery_semantics(runtime):
    context = SafetyExecutionContext("test", "release", "validate", {"value": 1})
    result = runtime.execute(SafetyRequest(context))
    assert __version__ == "1.0.0"
    assert context.capability_version == "1.0.0"
    assert result.capability_version == "1.0.0"
    assert result.recovery_result is None


def test_output_contract_failure_is_explicit(repository):
    registry = ComponentRegistry()
    registry.register(InvalidOutputComponent())
    runtime = SafetyRuntime(registry=registry, repository=repository)
    context = SafetyExecutionContext("test", "release", "validate", {"value": 1})
    result = runtime.execute(SafetyRequest(context))
    assert result.success is False
    assert result.error_code == "OUTPUT_VALIDATION_FAILED"


def test_repository_failure_preserves_original_result():
    registry = ComponentRegistry()
    registry.register(BasicValidationComponent())
    runtime = SafetyRuntime(registry=registry, repository=BrokenRepository())
    context = SafetyExecutionContext("test", "release", "validate", {"value": 1})
    result = runtime.execute(SafetyRequest(context))
    assert result.success is False
    assert result.error_code == "REPOSITORY_ERROR"
    assert result.details["original_result"]["success"] is True
