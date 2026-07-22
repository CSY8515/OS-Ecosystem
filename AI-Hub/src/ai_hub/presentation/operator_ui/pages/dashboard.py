from __future__ import annotations

from ai_hub.application.dashboard_query_service import DashboardSnapshot


def render_dashboard(snapshot: DashboardSnapshot, ui=None) -> None:
    if ui is None:
        import streamlit as ui

    ui.title("AI Hub")
    ui.caption(f"Operational snapshot · {snapshot.generated_at.isoformat()}")
    columns = ui.columns(4)
    columns[0].metric("Providers", len(snapshot.providers))
    columns[1].metric("Recent calls", snapshot.metrics.recent_calls)
    columns[2].metric(
        "Success rate",
        "Unknown" if snapshot.metrics.success_rate is None else f"{snapshot.metrics.success_rate:.1%}",
    )
    columns[3].metric("Router", snapshot.router_status)

    ui.subheader("Provider status")
    rows = [
        {
            "Provider": item.display_name,
            "Connected": item.connected,
            "Models": item.model_count,
            "Health": item.health,
            "Response time (ms)": item.response_time_ms,
            "Availability": item.availability,
            "Last check": item.last_check.isoformat() if item.last_check else "Unknown",
        }
        for item in snapshot.providers
    ]
    ui.dataframe(rows, width="stretch", hide_index=True)
    ui.caption("Raw prompts, responses, credentials, and provider exception payloads are not displayed.")
