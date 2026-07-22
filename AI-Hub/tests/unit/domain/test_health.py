from datetime import UTC, datetime

from ai_hub.application.health_service import HealthService
from ai_hub.domain.common.errors import ErrorCode, ProviderCallError
from ai_hub.domain.health import HealthRegistry, HealthState
from ai_hub.domain.providers import ModelRegistration, ProviderFamily, ProviderRegistration, ProviderResult


NOW = datetime(2026, 7, 22, tzinfo=UTC)
PROVIDER = ProviderRegistration("openai", ProviderFamily.OPENAI, "OpenAI", "OPENAI_KEY")
MODEL = ModelRegistration("openai-default", "openai", "native", frozenset({"generation"}))


class _Adapter:
    family = ProviderFamily.OPENAI
    def __init__(self, error=None): self.error = error
    def execute(self, *args):
        if self.error: raise self.error
        return ProviderResult(self.family, "openai-default", "OK")


def test_health_service_records_online_latency_and_availability() -> None:
    ticks = iter([1.0, 1.025])
    registry = HealthRegistry()
    result = HealthService(registry, lambda: next(ticks)).check(
        PROVIDER, MODEL, _Adapter(), "secret", checked_at=NOW, timeout_seconds=2
    )
    assert result.state == HealthState.ONLINE
    assert result.response_time_ms == 25
    assert result.availability == 1
    assert registry.latest("openai") == result


def test_retryable_failure_is_offline_and_updates_availability() -> None:
    registry = HealthRegistry()
    service = HealthService(registry, lambda: 1.0)
    service.check(PROVIDER, MODEL, _Adapter(), "secret", checked_at=NOW, timeout_seconds=2)
    result = service.check(
        PROVIDER, MODEL,
        _Adapter(ProviderCallError(ErrorCode.TIMEOUT, "timeout", retryable=True)),
        "secret", checked_at=NOW, timeout_seconds=2,
    )
    assert result.state == HealthState.OFFLINE
    assert result.availability == 0.5
    assert result.error_code == "timeout"


def test_disabled_provider_is_not_called() -> None:
    disabled = ProviderRegistration("openai", ProviderFamily.OPENAI, "OpenAI", "KEY", enabled=False)
    result = HealthService(HealthRegistry()).check(
        disabled, MODEL, _Adapter(error=AssertionError("must not call")), "secret", checked_at=NOW, timeout_seconds=2
    )
    assert result.state == HealthState.DISABLED
    assert result.availability is None
