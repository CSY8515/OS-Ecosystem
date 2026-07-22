from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from ai_hub.domain.router import RoutingPolicy


@dataclass(frozen=True, slots=True)
class HubSettings:
    default_provider_id: str | None = None
    auto_routing: bool = True
    retry_count: int = 2
    timeout_seconds: float = 30.0
    overall_timeout_seconds: float = 90.0
    health_check_interval_seconds: int = 300
    health_freshness_seconds: int = 600
    health_weight: float = 0.30
    suitability_weight: float = 0.25
    usage_weight: float = 0.20
    latency_weight: float = 0.15
    reliability_weight: float = 0.10
    usage_reserve_ratio: float = 0.05
    allow_unknown_health: bool = False
    log_retention_days: int = 30

    def __post_init__(self) -> None:
        if not self.auto_routing and not self.default_provider_id:
            raise ValueError("default provider is required when auto routing is disabled")
        if self.retry_count < 0 or self.retry_count > 10:
            raise ValueError("retry_count must be between 0 and 10")
        if self.timeout_seconds <= 0 or self.overall_timeout_seconds < self.timeout_seconds:
            raise ValueError("timeouts are invalid")
        if self.health_check_interval_seconds <= 0 or self.health_freshness_seconds <= 0:
            raise ValueError("health intervals must be positive")
        if self.log_retention_days <= 0:
            raise ValueError("log_retention_days must be positive")
        self.to_routing_policy("validation")

    def to_routing_policy(self, version: str) -> RoutingPolicy:
        return RoutingPolicy(
            version=version,
            health_weight=self.health_weight,
            suitability_weight=self.suitability_weight,
            usage_weight=self.usage_weight,
            latency_weight=self.latency_weight,
            reliability_weight=self.reliability_weight,
            allow_unknown_health=self.allow_unknown_health,
            usage_reserve_ratio=self.usage_reserve_ratio,
            auto_routing=self.auto_routing,
            default_provider_id=self.default_provider_id,
            retry_count=self.retry_count,
        )


@dataclass(frozen=True, slots=True)
class SettingsRevision:
    revision_id: str
    created_at: datetime
    actor_id: str
    settings: HubSettings

    def __post_init__(self) -> None:
        if not self.revision_id or not self.actor_id:
            raise ValueError("revision and actor identity are required")
