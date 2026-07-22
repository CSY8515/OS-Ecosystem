from ai_hub.domain.settings import SettingsRevision


def render_settings(revision: SettingsRevision | None, ui=None) -> None:
    if ui is None:
        import streamlit as ui
    ui.title("Settings")
    if revision is None:
        ui.warning("No settings revision is available.")
        return
    settings = revision.settings
    ui.caption(f"Revision {revision.revision_id} · {revision.created_at.isoformat()}")
    ui.json({
        "Default Provider": settings.default_provider_id,
        "Auto Routing": settings.auto_routing,
        "Retry Count": settings.retry_count,
        "Timeout": settings.timeout_seconds,
        "Health Check Interval": settings.health_check_interval_seconds,
    })
