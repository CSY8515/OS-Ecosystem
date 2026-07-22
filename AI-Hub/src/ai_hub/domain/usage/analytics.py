from __future__ import annotations

from dataclasses import dataclass
from collections.abc import Iterable

from ai_hub.domain.executions import ExecutionSummary


@dataclass(frozen=True, slots=True)
class UsageAnalytics:
    call_count: int
    success_count: int
    failure_count: int
    success_rate: float | None
    average_response_time_ms: float | None
    total_usage_units: int | None
    by_provider: tuple[tuple[str, int], ...]
    by_model: tuple[tuple[str, int], ...]


def build_usage_analytics(records: Iterable[ExecutionSummary]) -> UsageAnalytics:
    items = tuple(records)
    success_count = sum(item.success for item in items)
    provider_counts: dict[str, int] = {}
    model_counts: dict[str, int] = {}
    known_usage = [item.total_units for item in items if item.total_units is not None]
    for item in items:
        if item.provider_id:
            provider_counts[item.provider_id] = provider_counts.get(item.provider_id, 0) + 1
        if item.model_id:
            model_counts[item.model_id] = model_counts.get(item.model_id, 0) + 1
    return UsageAnalytics(
        call_count=len(items),
        success_count=success_count,
        failure_count=len(items) - success_count,
        success_rate=success_count / len(items) if items else None,
        average_response_time_ms=sum(item.duration_ms for item in items) / len(items) if items else None,
        total_usage_units=sum(known_usage) if known_usage else None,
        by_provider=tuple(sorted(provider_counts.items())),
        by_model=tuple(sorted(model_counts.items())),
    )
