from datetime import UTC, datetime

import pytest

from ai_hub.domain.health import HealthObservation, HealthState
from ai_hub.domain.providers import InferenceRequest, Message, ModelRegistration, ProviderFamily, ProviderRegistration
from ai_hub.domain.router import Router, RoutingCandidate, RoutingPolicy


REQUEST = InferenceRequest("r1", "living-os", "generation", (Message("user", "hello"),), 100)


def candidate(name: str, *, health=HealthState.ONLINE, latency=100.0, suitability=0.5, remaining=0.8, priority=100):
    provider = ProviderRegistration(name, ProviderFamily(name), name.title(), f"{name.upper()}_KEY")
    model = ModelRegistration(f"{name}-model", name, f"native-{name}", frozenset({"generation"}), routing_priority=priority, suitability=suitability, max_output_tokens=500)
    observation = HealthObservation(name, health, datetime(2026, 7, 22, tzinfo=UTC), latency, availability=0.99)
    return RoutingCandidate(provider, model, observation, remaining_usage_ratio=remaining, failure_rate=0.01)


def test_router_ranks_by_approved_weighted_evidence() -> None:
    slower = candidate("openai", latency=900, suitability=0.6)
    faster = candidate("gemini", latency=50, suitability=0.9)
    decision = Router().route(REQUEST, [slower, faster], RoutingPolicy())
    assert decision.selected.candidate.provider.provider_id == "gemini"
    assert len(decision.ordered_candidates) == 2


@pytest.mark.parametrize(
    "change, reason",
    [
        ({"credential_available": False}, "credential_unavailable"),
        ({"caller_allowed": False}, "caller_policy_denied"),
        ({"remaining_usage_ratio": 0.01}, "usage_limit_reached"),
    ],
)
def test_router_applies_hard_gates(change, reason) -> None:
    base = candidate("openai")
    values = {
        "provider": base.provider, "model": base.model, "health": base.health,
        "credential_available": True, "caller_allowed": True,
        "remaining_usage_ratio": base.remaining_usage_ratio, "failure_rate": base.failure_rate,
    }
    values.update(change)
    decision = Router().route(REQUEST, [RoutingCandidate(**values)], RoutingPolicy())
    assert decision.selected is None
    assert decision.exclusions == (("openai-model", reason),)


def test_unknown_health_requires_explicit_policy() -> None:
    base = candidate("openai")
    unknown = RoutingCandidate(base.provider, base.model, None, remaining_usage_ratio=0.8)
    assert Router().route(REQUEST, [unknown], RoutingPolicy()).selected is None
    assert Router().route(REQUEST, [unknown], RoutingPolicy(allow_unknown_health=True)).selected is not None


def test_default_provider_cannot_bypass_offline_gate() -> None:
    offline = candidate("openai", health=HealthState.OFFLINE)
    policy = RoutingPolicy(auto_routing=False, default_provider_id="openai")
    decision = Router().route(REQUEST, [offline], policy)
    assert decision.selected is None
    assert decision.exclusions[0][1] == "health_offline"


def test_tie_break_is_priority_then_stable_model_id() -> None:
    first = candidate("openai", priority=10)
    second = candidate("gemini", priority=20)
    decision = Router().route(REQUEST, [second, first], RoutingPolicy())
    assert decision.selected.candidate.model.model_id == "openai-model"


def test_attempt_plan_is_bounded_by_retry_count() -> None:
    candidates = [candidate("openai"), candidate("gemini"), candidate("claude")]
    decision = Router().route(REQUEST, candidates, RoutingPolicy(retry_count=1))
    assert len(decision.ordered_candidates) == 2
