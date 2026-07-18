from safety_capability import SafetyExecutionContext, SafetyRequest

def test_invalid_component_input_is_explicit(runtime, repository):
    context = SafetyExecutionContext("test", "unit", "validate", {})
    result = runtime.execute(SafetyRequest(context))
    assert result.success is False
    assert result.error_code == "INPUT_VALIDATION_FAILED"
    assert repository.count() == 1

def test_unknown_action_is_explicit(runtime):
    context = SafetyExecutionContext("test", "unit", "unknown", {"value": 1})
    result = runtime.execute(SafetyRequest(context))
    assert result.error_code == "ACTION_NOT_SUPPORTED"

def test_disabled_explicit_component_is_blocked(runtime):
    runtime.registry.set_enabled("basic-validation", False)
    context = SafetyExecutionContext("test", "unit", "validate", {"value": 1})
    result = runtime.execute(SafetyRequest(context, component_id="basic-validation"))
    assert result.error_code == "COMPONENT_DISABLED"

def test_missing_explicit_component_is_reported(runtime):
    context = SafetyExecutionContext("test", "unit", "validate", {"value": 1})
    result = runtime.execute(SafetyRequest(context, component_id="missing"))
    assert result.error_code == "COMPONENT_NOT_FOUND"

def test_non_string_component_id_is_invalid_context(runtime, repository):
    context = SafetyExecutionContext("test", "unit", "validate", {"value": 1})
    result = runtime.execute(SafetyRequest(context, component_id=123))
    assert result.error_code == "INVALID_CONTEXT"
    assert result.component_id == ""
    assert repository.get(context.request_id)["error_code"] == "INVALID_CONTEXT"
