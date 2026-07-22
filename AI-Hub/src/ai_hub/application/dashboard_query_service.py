from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Iterable


@dataclass(frozen=True, slots=True)
class ProviderDashboardRow:
    provider_id: str
    display_name: str
    enabled: bool
    connected: bool
    model_count: int
    health: str
    response_time_ms: float | None
    availability: float | None
    last_check: datetime | None


@dataclass(frozen=True, slots=True)
class DashboardMetrics:
    recent_calls: int = 0
    success_rate: float | None = None
    average_response_time_ms: float | None = None
    failover_count: int = 0
    usage_units: int | None = None


@dataclass(frozen=True, slots=True)
class DashboardSnapshot:
    generated_at: datetime
    providers: tuple[ProviderDashboardRow, ...]
    metrics: DashboardMetrics
    router_ready: bool
    router_status: str


class DashboardQueryService:
    def build_snapshot(
        self,
        *,
        generated_at: datetime,
        providers: Iterable[ProviderDashboardRow],
        metrics: DashboardMetrics,
    ) -> DashboardSnapshot:
        rows = tuple(sorted(providers, key=lambda row: row.provider_id))
        eligible = [row for row in rows if row.enabled and row.connected and row.health == "Online"]
        return DashboardSnapshot(
            generated_at=generated_at,
            providers=rows,
            metrics=metrics,
            router_ready=bool(eligible),
            router_status="Ready" if eligible else "No eligible provider",
        )
