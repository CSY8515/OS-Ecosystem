from ai_hub.domain.health import HealthState
from .models import RoutingCandidate, ScoredCandidate
from .policy import RoutingPolicy


def score_candidate(candidate: RoutingCandidate, policy: RoutingPolicy) -> ScoredCandidate:
    health = candidate.health
    if health and health.state == HealthState.ONLINE:
        health_score = health.availability if health.availability is not None else 1.0
    else:
        health_score = 0.5
    usage_score = candidate.remaining_usage_ratio if candidate.remaining_usage_ratio is not None else 0.5
    if health and health.response_time_ms is not None:
        latency_score = 1 / (1 + health.response_time_ms / 1000)
    else:
        latency_score = 0.5
    reliability_score = 1 - candidate.failure_rate if candidate.failure_rate is not None else 0.5
    components = (
        ("health", health_score),
        ("suitability", candidate.model.suitability),
        ("usage", usage_score),
        ("latency", latency_score),
        ("reliability", reliability_score),
    )
    score = (
        health_score * policy.health_weight
        + candidate.model.suitability * policy.suitability_weight
        + usage_score * policy.usage_weight
        + latency_score * policy.latency_weight
        + reliability_score * policy.reliability_weight
    )
    return ScoredCandidate(candidate, round(score, 9), components)
