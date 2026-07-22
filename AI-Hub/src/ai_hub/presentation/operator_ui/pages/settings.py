from ai_hub.domain.settings import SettingsRevision


def render_settings(revision: SettingsRevision | None, ui=None) -> None:
    if ui is None:
        import streamlit as ui
    ui.title("설정")
    if revision is None:
        ui.warning("사용 가능한 설정 개정본이 없습니다.")
        return
    settings = revision.settings
    ui.caption(f"설정 개정본 {revision.revision_id} · {revision.created_at:%Y-%m-%d %H:%M} UTC")
    ui.json({
        "기본 AI 제공자": settings.default_provider_id,
        "자동 라우팅": settings.auto_routing,
        "재시도 횟수": settings.retry_count,
        "제한 시간(초)": settings.timeout_seconds,
        "상태 확인 주기": settings.health_check_interval_seconds,
    })
