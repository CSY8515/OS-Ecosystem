from __future__ import annotations

from ai_hub.application.dashboard_query_service import DashboardSnapshot


def render_dashboard(snapshot: DashboardSnapshot, ui=None) -> None:
    if ui is None:
        import streamlit as ui

    ui.subheader("운영 현황")
    ui.caption(f"기준 시각 · {snapshot.generated_at:%Y-%m-%d %H:%M} UTC")
    columns = ui.columns(4)
    columns[0].metric("AI 제공자", len(snapshot.providers))
    columns[1].metric("최근 호출", snapshot.metrics.recent_calls)
    columns[2].metric(
        "성공률",
        "확인 전" if snapshot.metrics.success_rate is None else f"{snapshot.metrics.success_rate:.1%}",
    )
    router_status = {
        "No eligible provider": "제공자 없음",
        "Ready": "준비 완료",
    }.get(snapshot.router_status, snapshot.router_status)
    columns[3].metric("라우터", router_status)

    ui.subheader("AI 제공자 상태")
    rows = [
        {
            "AI 제공자": item.display_name,
            "연결": "연결됨" if item.connected else "연결 안 됨",
            "모델": item.model_count,
            "상태": {
                "Online": "정상",
                "Offline": "오프라인",
                "Degraded": "성능 저하",
                "Unknown": "확인 전",
            }.get(item.health, item.health),
            "응답 시간 (ms)": item.response_time_ms,
            "가용성": f"{item.availability:.1%}",
            "마지막 확인": f"{item.last_check:%Y-%m-%d %H:%M} UTC" if item.last_check else "확인 전",
        }
        for item in snapshot.providers
    ]
    if rows:
        ui.dataframe(rows, width="stretch", hide_index=True)
    else:
        ui.info(
            "연결된 AI 제공자가 없습니다. 배포 비밀값과 승인된 모델을 설정하면 "
            "상태가 표시됩니다. 현재 외부 AI 호출은 수행되지 않습니다."
        )
    ui.caption("원문 요청과 응답, 인증 정보, AI 제공자 예외 데이터는 표시하지 않습니다.")