import pytest
from safety_capability import SafetyExecutionContext, SafetyRequest

def test_runtime_executes_and_returns_common_result(runtime, repository):
    context = SafetyExecutionContext(source="test", target="unit", action="validate", payload={"value": 7})
    result = runtime.execute(SafetyRequest(context))
    assert result.success is True
    assert result.status == "SUCCESS"
    assert result.request_id == context.request_id
    assert result.component_id == "basic-validation"
    assert result.details["value"] == 7
    assert result.execution_time >= 0
    assert repository.count() == 1

def test_invalid_context_returns_and_records_failure(runtime, repository):
    context = SafetyExecutionContext(source="", target="unit", action="validate", payload={"value": 1})
    result = runtime.execute(SafetyRequest(context))
    assert result.success is False
    assert result.error_code == "INVALID_CONTEXT"
    assert repository.get(context.request_id)["error_code"] == "INVALID_CONTEXT"

def test_context_generates_unique_request_ids():
    first = SafetyExecutionContext("a", "b", "validate", {})
    second = SafetyExecutionContext("a", "b", "validate", {})
    assert first.request_id != second.request_id
    assert first.timestamp.tzinfo is not None

def test_non_request_is_rejected_as_programming_error(runtime):
    with pytest.raises(TypeError, match="SafetyRequest"):
        runtime.execute(None)

def test_mismatched_capability_version_is_explicit(runtime, repository):
    context = SafetyExecutionContext(
        "test", "unit", "validate", {"value": 1}, capability_version="0.1.0"
    )
    result = runtime.execute(SafetyRequest(context))
    assert result.error_code == "INVALID_CONTEXT"
    assert result.capability_version == "1.0.0"
    assert repository.get(context.request_id)["error_code"] == "INVALID_CONTEXT"
