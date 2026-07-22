from datetime import UTC, datetime

from ai_hub.application.dashboard_query_service import DashboardMetrics, DashboardQueryService
from ai_hub.presentation.operator_ui.pages.dashboard import render_dashboard


def build_initial_snapshot():
    return DashboardQueryService().build_snapshot(
        generated_at=datetime.now(UTC),
        providers=(),
        metrics=DashboardMetrics(),
    )


def main(ui=None) -> None:
    if ui is None:
        import streamlit as ui
    ui.set_page_config(page_title="AI Hub", page_icon="AI", layout="wide")
    render_dashboard(build_initial_snapshot(), ui)


if __name__ == "__main__":
    main()
