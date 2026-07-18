from safety_capability import BasicValidationComponent, ComponentRegistry, HealthStatus, SafetyRuntime

def test_health_reports_capability_and_component(runtime):
    report = runtime.health_check()
    assert report["capability"].status == HealthStatus.HEALTHY
    assert report["components"]["basic-validation"].status == HealthStatus.HEALTHY

def test_disabled_component_health_is_separate(runtime):
    runtime.registry.set_enabled("basic-validation", False)
    report = runtime.health_check()
    assert report["components"]["basic-validation"].status == HealthStatus.DISABLED
    assert report["capability"].status == HealthStatus.UNHEALTHY

def test_empty_runtime_health_is_unknown(repository):
    from safety_capability import SafetyRuntime
    runtime = SafetyRuntime(repository=repository)
    assert runtime.health_check()["capability"].status == HealthStatus.UNKNOWN

def test_invalid_component_health_report_is_isolated(repository):
    component = BasicValidationComponent()
    component.health_check = lambda: object()
    registry = ComponentRegistry()
    registry.register(component)
    runtime = SafetyRuntime(registry=registry, repository=repository)
    report = runtime.health_check()
    assert report["components"]["basic-validation"].status == HealthStatus.UNKNOWN
    assert report["capability"].status == HealthStatus.UNHEALTHY
