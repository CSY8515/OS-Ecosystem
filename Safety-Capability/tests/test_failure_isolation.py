from safety_capability import SafetyExecutionContext, SafetyRequest

def test_component_exception_is_isolated_and_runtime_continues(runtime, repository):
    failing = SafetyExecutionContext("test", "unit", "force_failure", {})
    failure = runtime.execute(SafetyRequest(failing))
    assert failure.success is False
    assert failure.error_code == "EXECUTION_FAILED"
    assert "intentional test failure" in failure.message

    succeeding = SafetyExecutionContext("test", "unit", "validate", {"value": "still-alive"})
    success = runtime.execute(SafetyRequest(succeeding))
    assert success.success is True
    assert repository.count() == 2

def test_execution_failure_can_be_retried(repository):
    from safety_capability import BasicValidationComponent, ComponentRegistry, SafetyRuntime
    registry = ComponentRegistry()
    registry.register(BasicValidationComponent())
    runtime = SafetyRuntime(registry=registry, repository=repository, max_retries=2)
    context = SafetyExecutionContext("test", "unit", "force_failure", {})
    result = runtime.execute(SafetyRequest(context))
    assert result.retry_count == 2
    assert result.error_code == "EXECUTION_FAILED"
