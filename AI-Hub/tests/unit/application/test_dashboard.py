from datetime import UTC, datetime

from ai_hub.application.dashboard_query_service import (
    DashboardMetrics,
    DashboardQueryService,
    ProviderDashboardRow,
)
from ai_hub.presentation.operator_ui.pages.dashboard import render_dashboard


def _provider(provider_id: str, health: str = "Online") -> ProviderDashboardRow:
    return ProviderDashboardRow(
        provider_id=provider_id,
        display_name=provider_id.title(),
        enabled=True,
        connected=True,
        model_count=1,
        health=health,
        response_time_ms=50.0,
        availability=0.99,
        last_check=datetime(2026, 7, 22, tzinfo=UTC),
    )


def test_dashboard_snapshot_is_sorted_and_router_ready() -> None:
    snapshot = DashboardQueryService().build_snapshot(
        generated_at=datetime(2026, 7, 22, tzinfo=UTC),
        providers=[_provider("openai"), _provider("claude")],
        metrics=DashboardMetrics(recent_calls=3, success_rate=2 / 3),
    )
    assert [row.provider_id for row in snapshot.providers] == ["claude", "openai"]
    assert snapshot.router_ready is True
    assert snapshot.router_status == "Ready"


class _Column:
    def __init__(self, calls): self.calls = calls
    def metric(self, label, value): self.calls.append(("metric", label, value))


class _UI:
    def __init__(self): self.calls = []
    def title(self, value): self.calls.append(("title", value))
    def caption(self, value): self.calls.append(("caption", value))
    def columns(self, count): return [_Column(self.calls) for _ in range(count)]
    def subheader(self, value): self.calls.append(("subheader", value))
    def dataframe(self, value, **kwargs): self.calls.append(("dataframe", value))


def test_dashboard_renderer_contains_only_operational_projection() -> None:
    snapshot = DashboardQueryService().build_snapshot(
        generated_at=datetime(2026, 7, 22, tzinfo=UTC),
        providers=[_provider("openai")],
        metrics=DashboardMetrics(),
    )
    ui = _UI()
    render_dashboard(snapshot, ui)
    rendered = repr(ui.calls)
    assert "Openai" in rendered
    assert "Raw prompts" in rendered
    assert "api_key" not in rendered
