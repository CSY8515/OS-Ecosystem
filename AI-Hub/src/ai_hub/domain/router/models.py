from __future__ import annotations

from dataclasses import dataclass

from ai_hub.domain.health import HealthObservation, HealthState
from ai_hub.domain.providers import ModelRegistration, ProviderRegistration


@dataclass(frozen=True, slots=True)
class RoutingCandidate:
    provider: ProviderRegistration
    model: ModelRegistration
    health: HealthObservation | None = None
    credential_available: bool = True
    caller_allowed: bool = True
    remaining_usage_ratio: float | None = None
    failure_rate: float | None = None

    def __post_init__(self) -> None:
        if self.model.provider_id != self.provider.provider_id:
            raise ValueError("model and provider registration do not match")
        for value in (self.remaining_usage_ratio, self.failure_rate):
            if value is not None and not 0 <= value <= 1:
                raise ValueError("routing ratios must be between zero and one")


@dataclass(frozen=True, slots=True)
class ScoredCandidate:
    candidate: RoutingCandidate
    score: float
    components: tuple[tuple[str, float], ...]


@dataclass(frozen=True, slots=True)
class RoutingDecision:
    policy_version: str
    ordered_candidates: tuple[ScoredCandidate, ...]
    exclusions: tuple[tuple[str, str], ...]

    @property
    def selected(self) -> ScoredCandidate | None:
        return self.ordered_candidates[0] if self.ordered_candidates else None
