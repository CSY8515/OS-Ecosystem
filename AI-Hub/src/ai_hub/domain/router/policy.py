from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class RoutingPolicy:
    version: str = "v0.1"
    health_weight: float = 0.30
    suitability_weight: float = 0.25
    usage_weight: float = 0.20
    latency_weight: float = 0.15
    reliability_weight: float = 0.10
    allow_unknown_health: bool = False
    usage_reserve_ratio: float = 0.05
    auto_routing: bool = True
    default_provider_id: str | None = None
    retry_count: int = 2

    def __post_init__(self) -> None:
        weights = (
            self.health_weight, self.suitability_weight, self.usage_weight,
            self.latency_weight, self.reliability_weight,
        )
        if any(value < 0 for value in weights) or abs(sum(weights) - 1.0) > 1e-9:
            raise ValueError("routing weights must be non-negative and total 1.0")
        if not 0 <= self.usage_reserve_ratio <= 1:
            raise ValueError("usage_reserve_ratio must be between zero and one")
        if self.retry_count < 0:
            raise ValueError("retry_count cannot be negative")
        if not self.auto_routing and not self.default_provider_id:
            raise ValueError("default_provider_id is required when auto routing is disabled")
