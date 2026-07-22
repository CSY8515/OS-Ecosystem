from datetime import UTC, datetime
from pathlib import Path

import pytest

from ai_hub.application.api_management_service import APIManagementService
from ai_hub.application.inference_service import InferenceService
from ai_hub.domain.callers import CallerRegistration
from ai_hub.domain.common.errors import ErrorCode, ProviderCallError
from ai_hub.domain.health import HealthObservation, HealthState
from ai_hub.domain.providers import (
    InferenceRequest, Message, ModelRegistration, ProviderFamily,
    ProviderRegistration, ProviderResult, Usage,
)
from ai_hub.domain.router import Router, RoutingCandidate, RoutingPolicy
from ai_hub.infrastructure.persistence import SQLiteExecutionRepository
from ai_hub.infrastructure.secrets import EnvironmentSecretResolver


NOW = datetime(2026, 7, 22, tzinfo=UTC)


class FakeAdapter:
    def __init__(self, family, *, output="ok", error=None):
        self.family, self.output, self.error, self.calls = family, output, error, 0
    def execute(self, request, model, credential, timeout_seconds):
        self.calls += 1
        assert credential == f"{self.family}-secret"
        if self.error:
            raise self.error
        return ProviderResult(self.family, model.model_id, self.output, Usage(2, 3, 5))


def candidate(family: ProviderFamily, suitability: float) -> RoutingCandidate:
    provider = ProviderRegistration(str(family), family, str(family).title(), f"{str(family).upper()}_KEY")
    model = ModelRegistration(
        f"{family}-model", str(family), f"native-{family}", frozenset({"generation", "structured_generation"}),
        suitability=suitability, max_output_tokens=4096,
    )
    health = HealthObservation(str(family), HealthState.ONLINE, NOW, 50, availability=1.0)
    return RoutingCandidate(provider, model, health, remaining_usage_ratio=0.9, failure_rate=0)


def service(tmp_path: Path, adapters):
    repository = SQLiteExecutionRepository(tmp_path / "hub.sqlite3")
    repository.migrate()
    api = APIManagementService()
    for caller in ("living-os", "universal-learning-engine"):
        api.register(CallerRegistration(caller, caller, frozenset({"inference"})))
    resolver = EnvironmentSecretResolver({
        "OPENAI_KEY": "openai-secret", "GEMINI_KEY": "gemini-secret", "CLAUDE_KEY": "claude-secret",
    })
    return InferenceService(
        router=Router(), adapters=adapters, secret_resolver=resolver,
        execution_repository=repository, api_management=api, clock=lambda: NOW,
        correlation_factory=lambda: "corr-1",
    ), repository


@pytest.mark.parametrize("caller", ["living-os", "universal-learning-engine"])
def test_registered_ecosystem_callers_receive_normalized_response(tmp_path: Path, caller: str) -> None:
    openai = FakeAdapter(ProviderFamily.OPENAI)
    hub, repository = service(tmp_path, {ProviderFamily.OPENAI: openai})
    request = InferenceRequest("request-1", caller, "generation", (Message("user", "hello"),))
    response = hub.execute(request, (candidate(ProviderFamily.OPENAI, 1),), RoutingPolicy(),
                           timeout_seconds=5, overall_timeout_seconds=10)
    assert response.success is True
    assert response.provider_id == "openai"
    assert response.usage.total_units == 5
    assert repository.recent()[0].caller_id == caller


def test_retryable_failure_fails_over_and_records_both_attempts(tmp_path: Path) -> None:
    openai = FakeAdapter(ProviderFamily.OPENAI, error=ProviderCallError(ErrorCode.TIMEOUT, "timeout", retryable=True))
    gemini = FakeAdapter(ProviderFamily.GEMINI, output="fallback")
    hub, repository = service(tmp_path, {ProviderFamily.OPENAI: openai, ProviderFamily.GEMINI: gemini})
    request = InferenceRequest("request-1", "living-os", "generation", (Message("user", "hello"),))
    response = hub.execute(
        request,
        (candidate(ProviderFamily.OPENAI, 1), candidate(ProviderFamily.GEMINI, 0.8)),
        RoutingPolicy(), timeout_seconds=5, overall_timeout_seconds=10,
    )
    assert response.output_text == "fallback"
    assert response.failover is True
    assert response.attempt_count == 2
    attempts = repository.attempts_for(response.correlation_id)
    assert [item.error_code for item in attempts] == ["timeout", None]
    assert attempts[1].retry is True


def test_non_retryable_failure_does_not_fail_over(tmp_path: Path) -> None:
    openai = FakeAdapter(ProviderFamily.OPENAI, error=ProviderCallError(ErrorCode.UNAUTHORIZED, "auth"))
    gemini = FakeAdapter(ProviderFamily.GEMINI)
    hub, _ = service(tmp_path, {ProviderFamily.OPENAI: openai, ProviderFamily.GEMINI: gemini})
    request = InferenceRequest("request-1", "living-os", "generation", (Message("user", "hello"),))
    response = hub.execute(request, (candidate(ProviderFamily.OPENAI, 1), candidate(ProviderFamily.GEMINI, 0.8)),
                           RoutingPolicy(), timeout_seconds=5, overall_timeout_seconds=10)
    assert response.success is False
    assert response.error_code == "unauthorized"
    assert gemini.calls == 0


def test_request_id_is_idempotent_within_runtime(tmp_path: Path) -> None:
    adapter = FakeAdapter(ProviderFamily.OPENAI)
    hub, repository = service(tmp_path, {ProviderFamily.OPENAI: adapter})
    request = InferenceRequest("same-request", "living-os", "generation", (Message("user", "hello"),))
    first = hub.execute(request, (candidate(ProviderFamily.OPENAI, 1),), RoutingPolicy(), timeout_seconds=5, overall_timeout_seconds=10)
    second = hub.execute(request, (candidate(ProviderFamily.OPENAI, 1),), RoutingPolicy(), timeout_seconds=5, overall_timeout_seconds=10)
    assert first == second
    assert adapter.calls == 1
    assert len(repository.recent()) == 1


def test_invalid_json_is_not_returned_or_failed_over(tmp_path: Path) -> None:
    openai = FakeAdapter(ProviderFamily.OPENAI, output="not json")
    gemini = FakeAdapter(ProviderFamily.GEMINI, output='{"ok": true}')
    hub, _ = service(tmp_path, {ProviderFamily.OPENAI: openai, ProviderFamily.GEMINI: gemini})
    request = InferenceRequest("request-1", "living-os", "structured_generation",
                               (Message("user", "json"),), response_format="json")
    response = hub.execute(request, (candidate(ProviderFamily.OPENAI, 1), candidate(ProviderFamily.GEMINI, 0.8)),
                           RoutingPolicy(), timeout_seconds=5, overall_timeout_seconds=10)
    assert response.error_code == "invalid_provider_response"
    assert gemini.calls == 0


def test_no_eligible_provider_returns_stable_failure_and_log(tmp_path: Path) -> None:
    adapter = FakeAdapter(ProviderFamily.OPENAI)
    hub, repository = service(tmp_path, {ProviderFamily.OPENAI: adapter})
    offline = candidate(ProviderFamily.OPENAI, 1)
    offline = RoutingCandidate(offline.provider, offline.model,
                               HealthObservation("openai", HealthState.OFFLINE, NOW, None))
    request = InferenceRequest("request-1", "living-os", "generation", (Message("user", "hello"),))
    response = hub.execute(request, (offline,), RoutingPolicy(), timeout_seconds=5, overall_timeout_seconds=10)
    assert response.error_code == "no_eligible_provider"
    assert response.attempt_count == 0
    assert repository.recent()[0].error_code == "no_eligible_provider"


def test_recording_failure_does_not_repeat_or_replace_success(tmp_path: Path) -> None:
    class BrokenRepository:
        def record(self, summary, attempts): raise RuntimeError("storage unavailable")
        def recent(self, limit=100): return ()

    adapter = FakeAdapter(ProviderFamily.OPENAI)
    api = APIManagementService()
    api.register(CallerRegistration("living-os", "Living OS", frozenset({"inference"})))
    hub = InferenceService(
        router=Router(), adapters={ProviderFamily.OPENAI: adapter},
        secret_resolver=EnvironmentSecretResolver({"OPENAI_KEY": "openai-secret"}),
        execution_repository=BrokenRepository(), api_management=api, clock=lambda: NOW,
        correlation_factory=lambda: "corr-broken-log",
    )
    request = InferenceRequest("request-1", "living-os", "generation", (Message("user", "hello"),))
    first = hub.execute(request, (candidate(ProviderFamily.OPENAI, 1),), RoutingPolicy(),
                        timeout_seconds=5, overall_timeout_seconds=10)
    second = hub.execute(request, (candidate(ProviderFamily.OPENAI, 1),), RoutingPolicy(),
                         timeout_seconds=5, overall_timeout_seconds=10)
    assert first.success is True
    assert second == first
    assert adapter.calls == 1
