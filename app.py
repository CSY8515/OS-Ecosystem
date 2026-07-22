"""OS Ecosystem v0.7.0 integrated product shell."""

from __future__ import annotations

import html
import os
import sys
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import urlparse

import streamlit as st


VERSION = "0.7.0"
AI_HUB_SOURCE = Path(__file__).resolve().parent / "AI-Hub" / "src"


@dataclass(frozen=True)
class Project:
    """Public OS System metadata. Internal implementation details stay private."""

    name: str
    label: str
    description: str
    url: str | None
    position: str


@dataclass(frozen=True)
class SixWMetadata:
    """Explain an ecosystem entry without exposing operational internals."""

    who: str
    when: str
    where: str
    what: str
    how: str
    why: str


@dataclass(frozen=True)
class Capability:
    name: str
    korean_name: str
    version: str
    status: str
    description: str
    anchor: str
    modules: tuple[str, ...]
    metadata: SixWMetadata


def _configured_url(name: str, default: str | None = None) -> str | None:
    """Return a safe HTTP(S) project URL from secrets, environment, or default."""
    value: str | None = None
    try:
        secret = st.secrets.get(name)
        if secret:
            value = str(secret)
    except Exception:
        pass
    value = value or os.getenv(name) or default
    if not value:
        return None
    parsed = urlparse(value.strip())
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        return None
    return value.strip()


def get_projects() -> tuple[Project, ...]:
    """Return public and repository-owned OS Systems."""
    return (
        Project("Living OS", "생활 운영", "삶의 기록과 운영을 하나의 흐름으로", _configured_url("LIVING_OS_URL", "https://living-os-h5uinmvmjpvv6m8phat28a.streamlit.app/"), "node-left"),
        Project("Universal Learning Engine", "학습 엔진", "어떤 주제든 구조화된 학습 경험으로", _configured_url("ULE_URL", "https://universal-learning-engine-zb5aezuadeu84gnqust8mw.streamlit.app/"), "node-right"),
        Project("AI Hub", "AI 운영", "모든 승인된 프로젝트를 위한 AI 라우팅과 운영", "?project=ai-hub", "node-bottom"),
    )


def get_project_metadata(project: Project) -> SixWMetadata:
    known = {
        "Living OS": SixWMetadata("개인 사용자와 Living OS", "사용자가 선택할 때", "독립 Streamlit 애플리케이션", "생활 기록과 운영", "공개 HTTPS UI로 직접 연결", "개인 생활 운영의 연속성을 제공"),
        "Universal Learning Engine": SixWMetadata("학습자와 Universal Learning Engine", "학습이 필요할 때", "독립 Streamlit 애플리케이션", "주제별 구조화 학습", "공개 HTTPS UI로 직접 연결", "반복 가능한 학습 경험을 제공"),
        "AI Hub": SixWMetadata("승인된 프로젝트와 운영자", "AI 요청과 상태 확인 시", "OS Ecosystem 내부 경로", "AI 제공자 중립 운영", "정책 기반 라우팅과 안전한 기록", "AI 사용을 한곳에서 통제하고 설명"),
    }
    return known.get(
        project.name,
        SixWMetadata("승인된 사용자", "사용자가 선택할 때", "등록된 애플리케이션", project.description, "승인된 경로로 연결", "등록 목적을 수행"),
    )


def get_capabilities() -> tuple[Capability, ...]:
    when, where = "공개 계약이 호출될 때", "OS Ecosystem Core"
    return (
        Capability("Safety Capability", "안전 역량", "v1.0.0", "안정", "검증, 통제된 실행, 실패 격리와 안전 기록을 제공합니다.", "cap-safety", ("검증 · Validation", "실행 · Execution", "상태 · Health"), SixWMetadata("모든 연결 시스템", when, where, "공통 안전 실행 기반", "검증과 격리 계약", "위험한 실행을 통제")),
        Capability("Enhancement Capability", "향상 역량", "v1.0.0", "안정", "분석, 학습, 패턴과 최적화를 위한 공통 기반입니다.", "cap-enhancement", ("분석 · Analytics", "학습 · Learning", "패턴 분석 · Pattern Analysis", "지식 관리 · Knowledge Management", "최적화 · Optimization", "규칙 생성 · Rule Generation"), SixWMetadata("분석이 필요한 프로젝트", when, where, "공통 분석과 개선", "결정론적 요청·결과 계약", "지속적인 개선 근거를 제공")),
        Capability("Automation Capability", "자동화 역량", "v1.0.0", "안정", "승인과 안전 검증을 포함한 공통 자동화 플랫폼입니다.", "automation", ("워크플로 · Workflow", "스케줄러 · Scheduler", "트리거 · Trigger", "루틴 · Routine", "자동 실행 · Auto Execution", "자동 결정 지원 · Auto Decision"), SixWMetadata("승인된 사용자와 프로젝트", when, where, "워크플로와 자동 실행", "검증→위험→승인→실행→기록", "반복 작업을 안전하게 수행")),
        Capability("Collaboration & Connectivity", "협업·연결 역량", "v1.0.0", "데모", "연결, 교환, 메시징과 동기화를 위한 제공자 중립 계약입니다.", "connectivity", ("레지스트리 · Registry", "계약 · Contracts", "가져오기·내보내기 · Import / Export", "메시징 · Messaging", "동기화 · Sync", "상태 · Health"), SixWMetadata("연결이 승인된 시스템", when, where, "공통 연결과 교환", "연결 어댑터와 안전 계약", "시스템 간 결합을 낮춤")),
        Capability("Personal Secretary Capability", "개인 비서 역량", "v1.0.0", "안정", "브리핑, 알림, 추천, 우선순위와 결정 지원을 제공합니다.", "secretary", ("브리핑 · Briefing", "검토 · Review", "알림 · Reminder", "추천 · Recommendation", "우선순위 · Priority", "결정 · Decision", "통지 · Notification"), SixWMetadata("사용자와 호출 프로젝트", when, where, "결정 지원과 요약", "결정론적 종합과 안전 검증", "다음 행동을 이해하기 쉽게 제안")),
    )


def _six_w_markup(metadata: SixWMetadata) -> str:
    fields = (("Who", "누가", metadata.who), ("When", "언제", metadata.when), ("Where", "어디서", metadata.where), ("What", "무엇을", metadata.what), ("How", "어떻게", metadata.how), ("Why", "왜", metadata.why))
    return '<dl class="six-w">' + "".join(f'<div><dt>{ko}<small>{en}</small></dt><dd>{html.escape(value)}</dd></div>' for en, ko, value in fields) + "</dl>"


def _project_node(project: Project) -> str:
    name, label, description = html.escape(project.name), html.escape(project.label), html.escape(project.description)
    role = "씨앗 · 성장 중인 내부 시스템" if project.name == "AI Hub" else "열매 · 독립 운영 시스템"
    role_class = "world-seed" if project.name == "AI Hub" else "world-fruit"
    classes = f"system-card project-node world-node {project.position} {role_class}"
    if project.url:
        url = html.escape(project.url, quote=True)
        external = project.url.startswith(("http://", "https://"))
        attrs = 'target="_blank" rel="noopener noreferrer"' if external else ""
        route = "새 탭에서 열기" if external else "현재 화면에서 열기"
        destination = "독립 앱" if external else "OS Ecosystem 내부"
        return f'<a class="{classes} is-action world-action" href="{url}" {attrs} data-destination="{destination}" aria-label="{name} {route}"><span class="interaction-hint">클릭하여 이동 <b aria-hidden="true">→</b></span><span class="world-symbol" aria-hidden="true"></span><span class="world-role">{role}</span><h3>{name}</h3><p>{description}</p><span class="card-action"><b>{label}</b><span>{destination} · {route}</span></span></a>'
    return f'<article class="{classes} is-unavailable world-landmark" aria-label="{name} 연결 준비 중"><span class="interaction-hint is-disabled">이동 불가</span><span class="world-symbol" aria-hidden="true"></span><span class="world-role">{role}</span><h3>{name}</h3><p>{description}</p><span class="card-note">승인된 배포 주소가 필요합니다. 연결 준비 중</span></article>'


def _project_metadata_card(project: Project) -> str:
    return f'<article class="metadata-card"><span class="card-type">시스템 맥락</span><h3>{html.escape(project.name)}</h3>{_six_w_markup(get_project_metadata(project))}</article>'


def _capability_card(item: Capability) -> str:
    modules = "".join(f"<span>{html.escape(module)}</span>" for module in item.modules)
    return f'<a class="capability-card is-action world-action" href="#{item.anchor}"><span class="interaction-hint">상세 정보 보기 <b aria-hidden="true">↓</b></span><span class="card-status">{item.status} · {item.version}</span><span class="card-type">성장 역량</span><h3>{item.korean_name}<small>{item.name}</small></h3><p>{item.description}</p><div class="module-list">{modules}</div>{_six_w_markup(item.metadata)}<span class="card-action"><b>역량 탐색</b><span>현재 페이지에서 이동</span></span></a>'


def _product_header_markup(current: str) -> str:
    items = (("홈", "Home", "./"), ("프로젝트", "Projects", "./#projects"), ("AI 허브", "AI Hub", "?project=ai-hub"), ("역량", "Capabilities", "./#capability"), ("거버넌스", "Governance", "./#governance"), ("아키텍처", "Architecture", "./#architecture"), ("레지스트리", "Registry", "./#registry"))
    parts = []
    for korean, english, href in items:
        current_class = ' class="is-current"' if current == english else ""
        current_attr = ' aria-current="page"' if current == english else ""
        parts.append(f'<a href="{href}"{current_class}{current_attr}><span>{korean}</span><small>{english}</small></a>')
    current_korean = next((korean for korean, english, _ in items if english == current), current)
    return f'<header class="product-header"><div class="product-identity"><a href="./" class="product-name">OS ECOSYSTEM</a><span class="product-version">v{VERSION} · 안정</span></div><nav class="ecosystem-nav" aria-label="OS Ecosystem 통합 메뉴">{"".join(parts)}</nav></header><div class="breadcrumb" aria-label="현재 위치"><a href="./">OS Ecosystem</a><span aria-hidden="true">/</span><strong>{current_korean}</strong></div>'


def _ai_hub_entry_action() -> str:
    return '<a class="button button-primary entry-action world-action" href="?project=ai-hub">AI Hub 운영 화면 열기 <span aria-hidden="true">→</span></a>'


def render_launcher(projects: tuple[Project, ...]) -> None:
    nodes = "".join(_project_node(project) for project in projects)
    capabilities = "".join(_capability_card(item) for item in get_capabilities())
    core_metadata = _six_w_markup(SixWMetadata("생태계 운영자와 사용자", "항상", "현재 저장소와 Streamlit 앱", "통합 운영 계층", "공개 계약과 레지스트리", "독립 시스템을 일관되게 연결"))
    st.html(f"""
    <main class="product-shell">
      {_product_header_markup("Home")}
      <section class="world-explorer" id="projects" aria-labelledby="world-title">
        <header class="world-intro">
          <div><span class="eyebrow">컨셉 인터페이스 · 통합 탐색 세계</span><h1 id="world-title">성장하는 시스템을<br>하나의 세계에서 탐색합니다.</h1><p>세계수는 현재 운영 중심, 열매는 독립 시스템, 씨앗은 내부 AI 허브를 의미합니다. 강조된 노드 전체를 클릭하면 표시된 목적지로 이동합니다.</p></div>
          <aside class="hero-status" aria-label="시스템 상태"><span class="status-dot"></span><strong>정상 운영 중</strong><small>시스템 정상 · v{VERSION}</small></aside>
        </header>
        <div class="interaction-guide" role="note" aria-label="탐색 방법">
          <span><i class="guide-action" aria-hidden="true"></i><b>강조 테두리 + 화살표</b> 클릭하여 이동</span>
          <span><i class="guide-landmark" aria-hidden="true"></i><b>얇은 테두리</b> 현재 위치 또는 정보</span>
          <span><i class="guide-route" aria-hidden="true"></i><b>카드 하단</b> 내부 이동·새 탭 이동 확인</span>
        </div>
        <div class="world-map" aria-label="OS 시스템 탐색 지도">
          <svg class="world-tree-view" viewBox="0 0 900 650" role="img" aria-label="OS Ecosystem Core에서 연결된 시스템으로 성장하는 세계수">
            <path class="tree-orbit" d="M155 270C220 80 680 80 745 270C805 455 650 590 450 598C250 590 95 455 155 270Z"/>
            <path class="tree-canopy" d="M450 100C342 100 275 162 282 243C207 257 188 358 255 400C278 470 366 476 423 435C480 486 581 468 603 397C681 357 657 251 582 239C587 157 540 100 450 100Z"/>
            <path class="tree-branch" d="M448 420C432 350 385 310 294 260M452 420C475 346 522 304 612 258M451 392C452 326 452 262 450 193"/>
            <path class="tree-trunk" d="M424 515C440 463 442 407 450 347C461 409 463 465 479 515Z"/>
            <path class="tree-root" d="M451 510C410 530 373 554 345 589M451 510C490 532 528 555 556 589M451 520L451 612"/>
            <circle class="tree-fruit" cx="285" cy="252" r="9"/><circle class="tree-fruit" cx="620" cy="250" r="9"/><ellipse class="tree-seed" cx="451" cy="615" rx="8" ry="13"/>
          </svg>
          {nodes}
          <article class="system-card core-card world-core world-landmark"><span class="interaction-hint is-current">현재 위치</span><span class="world-symbol" aria-hidden="true"></span><span class="world-role">세계수 · 운영 중심</span><h3>OS Ecosystem Core</h3><p>공통 역량, 거버넌스, 레지스트리와 제품 경험을 관리합니다.</p>{core_metadata}<span class="card-note">탐색 허브 · 이동 버튼이 아닌 현재 위치입니다.</span></article>
          <div class="growth-axis" aria-label="성장 단계"><span>씨앗<br><small>SEED · 가능성</small></span><b>→</b><span>성장<br><small>GROWTH · 역량</small></span><b>→</b><span>열매<br><small>FRUIT · 독립 시스템</small></span></div>
        </div>
        <details class="world-context"><summary>연결 이유와 책임 보기 <small>6하 원칙 메타데이터</small></summary><div class="metadata-grid">{"".join(_project_metadata_card(project) for project in projects)}</div></details>
      </section>
      <section class="product-section detail-section" id="ai-hub"><header class="section-heading"><div><span class="section-kicker">공식 프로젝트 · AI 운영</span><h2>AI Hub 운영 요약</h2></div><p>OS Ecosystem 저장소 안에서 함께 버전 관리되고 배포되는 공식 AI 운영 구성요소입니다.</p></header><div class="status-grid ai-hub-grid"><article class="info-card"><span>구성요소 버전</span><h3>v0.1.0</h3><p>OS Ecosystem v0.7.0 수명주기에 포함됩니다.</p></article><article class="info-card"><span>라우팅</span><h3>자동 선택</h3><p>상태와 정책에 따라 사용 가능한 AI 제공자를 선택합니다.</p></article><article class="info-card"><span>AI 제공자</span><h3>OpenAI / Gemini / Claude</h3><p>인증 정보는 배포 비밀값으로만 관리됩니다.</p></article><article class="info-card"><span>운영</span><h3>운영 화면 준비</h3><p>상태, 사용량, 라우팅과 실행 기록을 확인합니다.</p></article></div><div class="section-actions">{_ai_hub_entry_action()}</div></section>
      <section class="product-section" id="capability"><header class="section-heading"><div><span class="section-kicker">02 / 공통 역량</span><h2>공통 역량</h2></div><p>모든 역량은 OS Ecosystem Core 아래에서 동일한 메타데이터와 공개 계약을 사용합니다.</p></header><div class="capability-grid">{capabilities}</div></section>
      <section class="product-section detail-section" id="cap-safety"><header class="section-heading compact"><div><span class="section-kicker">CAP-01</span><h2>안전 역량</h2><small>Safety Capability</small></div><p>모든 실행 경로의 검증, 격리, 결과 기록을 담당합니다.</p></header><div class="flow"><span>검증<small>Validation</small></span><i>→</i><span>실행<small>Execution</small></span><i>→</i><span>격리<small>Isolation</small></span><i>→</i><span>기록<small>Record</small></span><i>→</i><span>상태<small>Health</small></span></div></section>
      <section class="product-section detail-section" id="cap-enhancement"><header class="section-heading compact"><div><span class="section-kicker">CAP-02</span><h2>향상 역량</h2><small>Enhancement Capability</small></div><p>프로젝트가 소유한 데이터를 이전하지 않고 분석과 개선 결과를 제공합니다.</p></header><div class="module-list detail-modules"><span>분석<small>Analytics</small></span><span>학습<small>Learning</small></span><span>패턴 분석<small>Pattern Analysis</small></span><span>지식 관리<small>Knowledge Management</small></span><span>최적화<small>Optimization</small></span><span>규칙 생성<small>Rule Generation</small></span></div></section>
      <section class="product-section detail-section" id="automation"><header class="section-heading compact"><div><span class="section-kicker">CAP-03 · 자동화 역량</span><h2>자동화 역량</h2><small>Automation Capability</small></div><p>명시적 승인과 안전 검증을 통과한 작업만 실행합니다.</p></header><div class="flow" aria-label="안전 검증을 포함한 자동화 흐름"><span>검증<small>Validation</small></span><i>→</i><span>위험 확인<small>Risk Check</small></span><i>→</i><span>승인<small>Approval</small></span><i>→</i><span>실행<small>Execution</small></span><i>→</i><span>기록<small>Logging</small></span><i>→</i><span>복구<small>Recovery</small></span></div><div class="status-grid automation-grid"><article class="info-card"><span>AUT-01</span><h3>워크플로<small>Workflow</small></h3><p>작업 순서를 정의합니다.</p></article><article class="info-card"><span>AUT-02</span><h3>스케줄러<small>Scheduler</small></h3><p>예약 실행을 관리합니다.</p></article><article class="info-card"><span>AUT-03</span><h3>트리거<small>Trigger</small></h3><p>이벤트와 조건을 평가합니다.</p></article><article class="info-card"><span>AUT-04</span><h3>루틴<small>Routine</small></h3><p>반복 루틴을 관리합니다.</p></article><article class="info-card"><span>AUT-05 · 승인 필요</span><h3>자동 실행<small>Auto Execution</small></h3><p>승인된 작업만 실행합니다.</p></article><article class="info-card"><span>AUT-06 · 제안 전용</span><h3>자동 결정 지원<small>Auto Decision</small></h3><p>설명 가능한 후보를 제안합니다.</p></article></div></section>
      <section class="product-section detail-section" id="connectivity"><header class="section-heading compact"><div><span class="section-kicker">CAP-04 · 협업·연결 역량</span><h2>협업·연결 역량</h2><small>Collaboration &amp; Connectivity</small></div><p>현재 상태는 실제 외부 연결이 아닌 명시적 로컬 시연입니다.</p></header><div class="status-grid"><article class="info-card"><span>역량 버전</span><h3>v1.0.0</h3><p>공개 연결 계약이 안정화되었습니다.</p></article><article class="info-card"><span>등록된 연결 어댑터</span><h3>데모 1개</h3><p>메모리 내 연결 어댑터 1개 · 사용 가능 1 · 성능 저하 0.</p></article><article class="info-card"><span>최근 상태 확인</span><h3>정상</h3><p>외부 서비스에 접속하지 않는 로컬 검사입니다.</p></article><article class="info-card"><span>최근 연결 결과</span><h3>데모 준비</h3><p>승인된 어댑터를 연결할 준비가 되었습니다.</p></article></div><p class="integration-note">안전 검증 → 연결 실행 → 정제된 기록 → 향상 분석 · 자동화 역량도 같은 요청 계약을 사용할 수 있습니다.</p></section>
      <section class="product-section detail-section" id="secretary"><header class="section-heading compact"><div><span class="section-kicker">CAP-05 · 개인 비서 역량</span><h2>개인 비서 역량</h2><small>Personal Secretary</small></div><p>데이터와 실행 권한을 원래 시스템에 남겨둔 채 결정 지원 정보를 제공합니다.</p></header><div class="status-grid"><article class="info-card"><span>역량 버전</span><h3>v1.0.0</h3><p>안정적이고 결정론적인 프로젝트 중립 공개 계약입니다.</p></article><article class="info-card"><span>오늘의 브리핑</span><h3>준비 완료</h3><p>호출자가 제공한 입력 스냅샷으로 브리핑합니다.</p></article><article class="info-card"><span>대기 중인 알림</span><h3>원본 시스템 관리</h3><p>일정과 영구 데이터는 원래 프로젝트가 소유합니다.</p></article><article class="info-card"><span>추천 생성</span><h3>요청 시 생성</h3><p>요청 시 투명한 기준으로 순위를 계산합니다.</p></article><article class="info-card"><span>알림 상태</span><h3>중복 방지</h3><p>활성 세션의 반복 알림을 억제합니다.</p></article></div><div class="flow" aria-label="개인 비서 결정 지원 흐름"><span>Living OS / ULE</span><i>→</i><span>정보 종합<small>Synthesis</small></span><i>→</i><span>안전 검증<small>Safety Check</small></span><i>→</i><span>추천<small>Recommendation</small></span><i>→</i><span>사용자 결정<small>User Decision</small></span></div><p class="integration-note">일일 브리핑 · 주간 검토 · 월간 검토 · 스마트 알림 · 추천 엔진 · 우선순위 관리 · 결정 지원 · 알림 관리</p></section>
      <section class="product-section" id="governance"><header class="section-heading"><div><span class="section-kicker">03 / 거버넌스</span><h2>운영 거버넌스</h2></div><p>Ultra Brain 전용 거버넌스를 해석하거나 대체하지 않고 OS Ecosystem 운영 책임만 관리합니다.</p></header><div class="boundary-banner"><strong>책임 경계</strong><span>OS Ecosystem: 연결·등록·호환성·검증·릴리스</span><span>Ultra Brain: 전용 최상위 거버넌스 — 본 제품 범위 밖</span></div><div class="status-grid governance-grid"><article class="info-card"><span>GOV-01</span><h3>생태계 헌장<small>Ecosystem Constitution</small></h3><p>권한, 프로젝트 자율성, 소유권과 생태계 계층의 경계를 정의합니다.</p></article><article class="info-card"><span>GOV-02</span><h3>생태계 규칙<small>Ecosystem Rules</small></h3><p>프로젝트 연결, 승인된 변경, 릴리스와 운영 책임을 관리합니다.</p></article><article class="info-card"><span>GOV-03</span><h3>생태계 원칙<small>Ecosystem Principles</small></h3><p>현재 PRINCIPLES.md 원문을 유지합니다. 별도 6대 운영 원칙은 공식 문서 확인 후 반영합니다.</p></article><article class="info-card"><span>GOV-04</span><h3>생태계 표준<small>Ecosystem Standards</small></h3><p>호환성, 문서, 테스트와 릴리스의 공통 기준을 정의합니다.</p></article><article class="info-card"><span>GOV-05</span><h3>생태계 정책<small>Ecosystem Policies</small></h3><p>승인, 유지보수, 폐기, 보안과 공개 정책을 기록합니다.</p></article></div></section>
      <section class="product-section" id="architecture"><header class="section-heading"><div><span class="section-kicker">04 / 아키텍처</span><h2>제품 아키텍처</h2></div><p>소유권과 배포 경계를 유지하면서 각 계층이 바로 아래 계층만 관리합니다.</p></header><div class="hierarchy"><span>OS 생태계<small>OS ECOSYSTEM</small></span><b>→</b><span>OS 시스템<small>OS SYSTEM</small></span><b>→</b><span>역량<small>CAPABILITY</small></span><b>→</b><span>모듈<small>MODULE</small></span></div><div class="status-grid architecture-grid"><article class="info-card"><span>ARC-01</span><h3>마스터 아키텍처<small>Master Architecture</small></h3><p>OS Ecosystem은 독립 프로젝트 실행 환경을 연결하는 거버넌스, 레지스트리와 탐색 계층입니다.</p></article><article class="info-card"><span>ARC-02</span><h3>저장소 전략<small>Repository Strategy</small></h3><p>독립 프로젝트는 독립 저장소를 유지하고 AI Hub는 현재 저장소에 남습니다.</p></article><article class="info-card"><span>ARC-03</span><h3>통합 전략<small>Integration Strategy</small></h3><p>독립 프로젝트는 공개 계약과 직접 링크를 사용하고, AI Hub는 내부 패키지와 애플리케이션 경로를 사용합니다.</p></article><article class="info-card"><span>ARC-04</span><h3>로드맵<small>Roadmap</small></h3><p>공식 6대 운영 원칙 반영은 원문 확보 후 진행합니다.</p></article><article class="info-card"><span>ARC-05</span><h3>역량 아키텍처<small>Capability Architecture</small></h3><p>Safety, Enhancement, Automation, Collaboration &amp; Connectivity, Personal Secretary가 운영 중심 하위의 공개 계약을 사용합니다.</p></article><article class="info-card"><span>ARC-06</span><h3>6하 원칙 메타데이터<small>6W Metadata</small></h3><p>누가, 언제, 어디서, 무엇을, 어떻게, 왜를 설명과 추적성의 공통 계약으로 사용합니다.</p></article><article class="info-card"><span>ARC-07</span><h3>공통 UI 시스템<small>Common UI System</small></h3><p>세계수, 열매, 씨앗과 성장 언어를 실제 탐색 컴포넌트로 표준화합니다.</p></article></div></section>
      <section class="product-section" id="registry"><header class="section-heading"><div><span class="section-kicker">05 / 레지스트리</span><h2>통합 레지스트리</h2></div><p>화면과 문서가 같은 분류, 버전, 경로와 상태 언어를 사용합니다.</p></header><div class="status-grid registry-grid"><article class="info-card registry-item"><span>REG-01</span><h3>프로젝트 레지스트리<small>Project Registry</small></h3><div class="registry-row"><span>OS Ecosystem Core</span><b>v{VERSION} · 운영 중</b></div><div class="registry-row"><span>AI Hub</span><b>v0.1.0 · 통합</b></div><div class="registry-row"><span>Living OS</span><b>v2.0.4 · 안정</b></div><div class="registry-row"><span>Universal Learning Engine</span><b>v1.0.0 · 안정</b></div></article><article class="info-card registry-item"><span>REG-02</span><h3>역량 레지스트리<small>Capability Registry</small></h3><div class="registry-row"><span>Safety Capability</span><b>v1.0.0 · 안정</b></div><div class="registry-row"><span>Enhancement Capability</span><b>v1.0.0 · 안정</b></div><div class="registry-row"><span>Automation Capability</span><b>v1.0.0 · 안정</b></div><div class="registry-row"><span>Collaboration &amp; Connectivity</span><b>v1.0.0 · 데모</b></div><div class="registry-row"><span>Personal Secretary</span><b>v1.0.0 · 안정</b></div><p>역량 식별자와 승인된 모듈 범위만 공개하며 실행 환경 내부는 거버넌스에 따라 숨깁니다.</p></article><article class="info-card registry-item"><span>REG-03</span><h3>릴리스 이력<small>Release History</small></h3><div class="registry-row"><span>v0.7.0</span><b>제품 통합</b></div><div class="registry-row"><span>v0.6.2</span><b>AI Hub 플랫폼 통합</b></div><div class="registry-row"><span>v0.6.1</span><b>AI Hub 프로젝트 진입점</b></div><div class="registry-row"><span>v0.6.0</span><b>개인 비서</b></div><div class="registry-row"><span>v0.5.0</span><b>협업·연결</b></div><div class="registry-row"><span>v0.4.4</span><b>문서 표준화</b></div><div class="registry-row"><span>v0.4.3</span><b>자동화 역량</b></div><div class="registry-row"><span>v0.3.3</span><b>향상 역량</b></div></article></div></section>
      <footer class="product-footer"><span>OS ECOSYSTEM · v{VERSION}</span><span>서울 · KST</span></footer>
    </main>""")


def apply_theme() -> None:
    st.html("""<style>
    :root{--font-ui:"Pretendard Variable",Pretendard,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;--font-display:var(--font-ui);--bg:#071011;--panel:#0a1718;--panel2:#0d1d1e;--ink:#edf4f3;--muted:#809496;--line:rgba(143,225,219,.18);--line-strong:rgba(143,225,219,.48);--cyan:#8fe1db;--green:#75e3ae;--soil:#a18b6d}html,body,[data-testid="stAppViewContainer"]{background:var(--bg)}[data-testid="stHeader"],[data-testid="stSidebar"],[data-testid="stToolbar"],footer{display:none!important}.stApp{color:var(--ink);background:radial-gradient(circle at 12% 18%,rgba(143,225,219,.08) 0 1px,transparent 2px),radial-gradient(circle at 78% 12%,rgba(255,255,255,.07) 0 1px,transparent 2px),radial-gradient(circle at 62% 63%,rgba(143,225,219,.05) 0 1px,transparent 2px),var(--bg);background-size:180px 180px,260px 260px,220px 220px}.block-container{max-width:none;padding:0!important}[data-testid="stAppViewContainer"]:has(.integrated-platform) .block-container{max-width:1180px;padding:0 30px 72px!important}.product-shell,.integrated-platform{min-height:100vh;color:var(--ink);font-family:var(--font-ui)}
    .product-header{position:sticky;top:0;z-index:20;display:flex;align-items:center;justify-content:space-between;gap:26px;padding:18px clamp(20px,4vw,58px);border-bottom:1px solid var(--line);background:rgba(7,16,17,.96);}.product-identity{display:flex;align-items:center;gap:14px;white-space:nowrap}.product-name{color:var(--ink)!important;text-decoration:none!important;font:600 14px/1 var(--font-display);letter-spacing:.08em}.product-version{color:var(--green);font-size:9px;letter-spacing:.12em}.ecosystem-nav{display:flex;align-items:center;gap:3px;scrollbar-width:thin;scrollbar-color:var(--line-strong) transparent}.ecosystem-nav::-webkit-scrollbar{height:2px}.ecosystem-nav::-webkit-scrollbar-thumb{background:var(--line-strong)}.ecosystem-nav a{display:flex;flex-direction:column;gap:3px;min-width:72px;padding:9px 11px;color:var(--muted)!important;text-decoration:none!important;border:1px solid transparent;text-align:center}.ecosystem-nav a span{font-size:11px}.ecosystem-nav a small{font-size:7px;letter-spacing:.12em;text-transform:uppercase}.ecosystem-nav a:hover,.ecosystem-nav a:focus-visible,.ecosystem-nav a.is-current{color:var(--cyan)!important;border-color:var(--line-strong);background:rgba(143,225,219,.06);outline:none}.breadcrumb{display:flex;gap:9px;align-items:center;padding:18px clamp(20px,4vw,58px);color:#667b7d;font-size:10px}.breadcrumb a{color:#9bb0b1!important;text-decoration:none!important}.breadcrumb strong{color:var(--cyan);font-weight:500}
    .world-explorer{max-width:1320px;margin:0 auto;padding:38px clamp(22px,4vw,56px) 86px;scroll-margin-top:80px}.world-intro{display:grid;grid-template-columns:minmax(0,1fr) 250px;align-items:end;gap:48px;margin-bottom:22px}.eyebrow,.section-kicker,.card-type,.info-card>span{color:#8aa0a1;font-size:10px;letter-spacing:.17em}.world-intro h1{max-width:850px;margin:16px 0 20px;font:600 clamp(38px,5vw,66px)/1.05 var(--font-display);letter-spacing:-.045em}.world-intro p{max-width:720px;margin:0;color:#9badad;font-size:14px;line-height:1.75}.hero-status{padding:20px;border:1px solid var(--line);background:rgba(10,23,24,.94);display:grid;grid-template-columns:auto 1fr;gap:5px 10px}.hero-status .status-dot{grid-row:1/3;width:7px;height:7px;margin-top:4px;border-radius:50%;background:var(--green)}.hero-status strong{font-size:12px}.hero-status small{color:var(--muted);font-size:8px;letter-spacing:.1em}.interaction-guide{display:flex;flex-wrap:wrap;gap:10px 24px;padding:14px 16px;border:1px solid var(--line);background:#081314;color:#849798;font-size:10px}.interaction-guide span{display:flex;align-items:center;gap:8px}.interaction-guide b{color:#c8d5d4;font-weight:500}.interaction-guide i{width:14px;height:10px;border:1px solid var(--line);background:var(--panel)}.interaction-guide .guide-action{border-color:var(--cyan);border-right-width:3px}.interaction-guide .guide-landmark{border-color:#526466}.interaction-guide .guide-route{border-bottom-color:var(--cyan)}
    .world-map{position:relative;min-height:720px;margin-top:18px;overflow:hidden;border:1px solid var(--line);background:linear-gradient(180deg,rgba(8,20,21,.62),rgba(5,13,14,.9))}.world-map:before{content:"대화형 시스템 지도";position:absolute;top:18px;left:20px;color:#829798;font-size:9px;letter-spacing:.18em}.world-tree-view{position:absolute;left:50%;top:26px;width:min(68%,780px);height:650px;transform:translateX(-50%);pointer-events:none}.tree-orbit{fill:none;stroke:rgba(143,225,219,.11);stroke-width:1;stroke-dasharray:4 8}.tree-canopy{fill:rgba(61,104,87,.08);stroke:rgba(117,227,174,.22);stroke-width:1.2}.tree-branch,.tree-trunk,.tree-root{fill:none;stroke:rgba(143,225,219,.28);stroke-width:2}.tree-trunk{fill:rgba(71,99,86,.15);stroke-width:1.5}.tree-fruit{fill:#0b1718;stroke:rgba(143,225,219,.55);stroke-width:2}.tree-seed{fill:rgba(161,139,109,.12);stroke:rgba(161,139,109,.7);stroke-width:2}
    .system-card,.capability-card,.info-card,.metadata-card{box-sizing:border-box;border:1px solid var(--line);background:rgba(10,23,24,.97);color:var(--ink);padding:24px;text-decoration:none}.system-card h3,.capability-card h3,.info-card h3,.metadata-card h3{margin:16px 0 9px;font:600 19px/1.25 var(--font-display)}.system-card p,.capability-card p,.info-card p{margin:0;color:var(--muted);font-size:12px;line-height:1.65}.world-node,.world-core{position:absolute;width:min(28%,320px);z-index:3}.node-left{left:3.5%;top:70px}.node-right{right:3.5%;top:70px}.node-bottom{left:50%;bottom:24px;transform:translateX(-50%)}.world-core{left:50%;top:218px;transform:translateX(-50%);width:292px;background:linear-gradient(145deg,rgba(14,39,35,.97),rgba(8,20,21,.98));border-color:rgba(117,227,174,.32)}.world-role{display:block;color:#8aa0a1;font-size:9px;letter-spacing:.13em}.world-symbol{display:block;position:relative;width:30px;height:30px;margin-bottom:15px;border:1px solid var(--line-strong)}.world-fruit .world-symbol{border-radius:50% 44% 50% 46%;transform:rotate(-8deg)}.world-fruit .world-symbol:after{content:"";position:absolute;width:9px;height:5px;right:-5px;top:-4px;border:1px solid var(--green);border-left:0;border-bottom:0;transform:rotate(-18deg)}.world-seed .world-symbol{width:20px;height:32px;border-radius:52% 48% 55% 45%;border-color:rgba(161,139,109,.8)}.world-core .world-symbol{width:34px;height:36px;border:0;border-bottom:2px solid var(--green)}.world-core .world-symbol:before,.world-core .world-symbol:after{content:"";position:absolute;bottom:0;width:24px;height:24px;border:1px solid rgba(117,227,174,.55);border-radius:50%}.world-core .world-symbol:before{left:-7px}.world-core .world-symbol:after{right:-7px}.interaction-hint{float:right;display:flex;align-items:center;gap:8px;padding:6px 8px;border:1px solid var(--cyan);color:var(--cyan);font-size:9px;letter-spacing:.05em}.interaction-hint.is-current,.interaction-hint.is-disabled{border-color:#526466;color:#9aabad}.world-action{position:relative;display:block;cursor:pointer;border-color:var(--line-strong)!important;transition:transform .16s ease,border-color .16s ease,background .16s ease}.world-action:hover,.world-action:focus-visible{background:#0d1d1e;border-color:var(--cyan)!important;transform:translateY(-3px);outline:3px solid rgba(143,225,219,.13);outline-offset:3px}.node-bottom:hover,.node-bottom:focus-visible{transform:translateX(-50%) translateY(-3px)}.card-status{float:right;color:#a9b9b9;font-size:9px;letter-spacing:.1em}.card-status.is-ready{color:var(--green)}.card-action{display:flex;justify-content:space-between;gap:12px;align-items:flex-end;margin-top:22px;padding-top:14px;border-top:1px solid var(--line);color:var(--cyan);font-size:9px}.card-action b{font-size:10px}.card-action span{text-align:right;color:#91a7a7}.card-note{display:block;margin-top:22px;padding-top:14px;border-top:1px solid var(--line);color:#718586;font-size:9px}.growth-axis{position:absolute;left:20px;bottom:18px;display:flex;align-items:center;gap:8px;color:#8ea1a2;font-size:9px;letter-spacing:.1em}.growth-axis b{color:var(--cyan)}.growth-axis small{color:#7f9495;font-size:8px}.world-context{margin-top:14px;border:1px solid var(--line);background:#081314}.world-context summary{cursor:pointer;padding:16px 18px;color:#c8d5d4;font-size:11px;list-style:none}.world-context summary::-webkit-details-marker{display:none}.world-context summary:after{content:"＋";float:right;color:var(--cyan)}.world-context[open] summary:after{content:"−"}.world-context summary small{margin-left:8px;color:#6f8384;font-size:8px;letter-spacing:.12em}.metadata-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:1px;padding:1px;background:rgba(143,225,219,.08)}.metadata-card{border:0}.metadata-card h3{font-size:15px}
    .product-section{max-width:1220px;margin:0 auto;padding:88px clamp(24px,5vw,72px);border-top:1px solid rgba(143,225,219,.09);scroll-margin-top:90px}.detail-section{padding-top:70px;padding-bottom:70px}.section-heading{display:grid;grid-template-columns:minmax(280px,.8fr) 1.2fr;gap:40px;align-items:end;margin-bottom:34px}.section-heading h2{margin:10px 0 0;font:600 clamp(28px,4vw,43px)/1.08 var(--font-display);letter-spacing:-.04em}.section-heading p{margin:0;color:var(--muted);font-size:12px;line-height:1.75}.section-heading small{display:block;margin-top:7px;color:#6f8384;font-size:10px}.section-heading.compact h2{font-size:31px}.capability-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:14px}.capability-card h3 small{display:block;margin-top:7px;color:#6f8384;font-size:10px}
    .six-w{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:1px;margin:20px 0 0;background:rgba(143,225,219,.08)}.six-w div{padding:9px;background:#081314}.six-w dt{color:var(--cyan);font-size:9px;letter-spacing:.08em}.six-w dt small{margin-left:5px;color:#688082}.six-w dd{margin:5px 0 0;color:#a8b8b8;font-size:10px;line-height:1.45}.module-list{display:flex;flex-wrap:wrap;gap:6px;margin-top:18px}.module-list span{padding:7px 9px;border:1px solid rgba(143,225,219,.16);color:#a7b7b7;font-size:9px}.module-list span small,.flow span small,.hierarchy span small,.info-card h3 small{display:block;margin-top:4px;color:#718788;font-size:8px;font-weight:400;letter-spacing:.04em}.detail-modules{padding:22px;border:1px solid var(--line);background:var(--panel)}
    .status-grid{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:1px;background:rgba(143,225,219,.08);padding:1px}.status-grid .info-card{border:0;min-height:180px}.automation-grid,.governance-grid,.architecture-grid,.registry-grid{grid-template-columns:repeat(3,minmax(0,1fr))}.section-actions{margin-top:22px}.button{display:inline-flex;align-items:center;gap:16px;padding:13px 17px;border:1px solid var(--cyan);color:#071011!important;background:var(--cyan);text-decoration:none!important;font-size:11px;font-weight:600}.button:hover,.button:focus-visible{background:#b8f0ec;outline:3px solid rgba(143,225,219,.18);outline-offset:3px}.flow,.hierarchy,.boundary-banner{display:flex;align-items:center;justify-content:center;flex-wrap:wrap;gap:12px;padding:20px;border:1px solid var(--line);background:var(--panel);color:#b7c6c6;font-size:10px}.flow i,.hierarchy b{color:var(--cyan);font-style:normal}.integration-note{color:#718586;font-size:9px;letter-spacing:.06em}.boundary-banner{justify-content:flex-start;margin-bottom:18px}.boundary-banner strong{color:var(--cyan)}.boundary-banner span{padding-left:14px;border-left:1px solid var(--line)}.hierarchy{margin-bottom:18px}.registry-row{display:flex;justify-content:space-between;gap:12px;padding:11px 0;border-bottom:1px solid rgba(143,225,219,.08);font-size:9px}.registry-row b{color:var(--cyan);font-size:9px;text-align:right}.product-footer{display:flex!important;justify-content:space-between;max-width:1220px;margin:0 auto;padding:28px clamp(24px,5vw,72px);border-top:1px solid var(--line);color:#7c9192;font-size:9px;letter-spacing:.14em}
    [data-testid="stAppViewContainer"]:has(.integrated-platform) h1,[data-testid="stAppViewContainer"]:has(.integrated-platform) h2,[data-testid="stAppViewContainer"]:has(.integrated-platform) h3{color:var(--ink);font-family:var(--font-display)}[data-testid="stAppViewContainer"]:has(.integrated-platform) [data-testid="stMetric"]{padding:18px;border:1px solid var(--line);background:var(--panel)}[data-testid="stAppViewContainer"]:has(.integrated-platform) [data-testid="stMetricLabel"] p{color:#aababa}[data-testid="stAppViewContainer"]:has(.integrated-platform) [data-testid="stAlert"]{border:1px solid var(--line-strong);border-radius:0!important;background:var(--panel)!important;color:var(--ink)!important}[data-testid="stAppViewContainer"]:has(.integrated-platform) [data-testid="stAlert"]>div{background:var(--panel)!important;color:var(--ink)!important}[data-testid="stAppViewContainer"]:has(.integrated-platform) [data-testid="stAlert"] p{color:#b7c6c6}[data-testid="stAppViewContainer"]:has(.integrated-platform) [data-testid="stSpinner"]{color:var(--cyan)}[data-testid="stAppViewContainer"]:has(.integrated-platform) [data-testid="stDataFrame"]{border:1px solid var(--line)}.platform-intro{position:relative;margin:40px 0 26px;padding:30px 30px 30px 96px;border:1px solid var(--line);background:linear-gradient(110deg,rgba(10,23,24,.96),rgba(8,19,20,.76))}.platform-intro h1{margin:8px 0;font-size:40px}.platform-intro p{color:var(--muted)}.platform-landmark{position:absolute;left:28px;top:33px;width:40px;height:50px;border:1px solid rgba(161,139,109,.75);border-radius:52% 48% 55% 45%}.platform-landmark:after{content:"씨앗";position:absolute;top:56px;left:1px;color:#7f735f;font-size:7px;letter-spacing:.12em}.state-panel{padding:22px;border:1px solid var(--line);background:var(--panel);margin:18px 0}.state-panel strong{display:block;color:var(--ink);margin-bottom:7px}.state-panel p{margin:0;color:var(--muted);font-size:12px}
    @media(max-width:1050px){.product-header{position:relative;align-items:flex-start;flex-direction:column}.ecosystem-nav{width:100%;overflow-x:auto;justify-content:flex-start}.ecosystem-nav a{min-width:78px}.world-intro{grid-template-columns:1fr}.world-map{min-height:auto;padding:80px 18px 24px;display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:12px}.world-tree-view{opacity:.38;top:10px;width:90%}.world-node,.world-core{position:relative;inset:auto;width:auto;transform:none!important}.world-core{grid-column:1/-1}.node-bottom{grid-column:1/-1}.growth-axis{position:relative;left:auto;bottom:auto;grid-column:1/-1;margin-top:8px}.metadata-grid{grid-template-columns:1fr}.capability-grid{grid-template-columns:1fr}.status-grid,.automation-grid,.governance-grid,.architecture-grid,.registry-grid{grid-template-columns:repeat(2,minmax(0,1fr))}.section-heading{grid-template-columns:1fr;gap:15px}}@media(max-width:520px){.product-header{padding:14px 16px}.product-identity{width:100%;justify-content:space-between}.ecosystem-nav a{min-width:70px;padding:8px}.breadcrumb{padding:15px 18px}.world-explorer{padding:26px 18px 54px}.world-intro{gap:16px;margin-bottom:16px}.world-intro h1{margin:12px 0 14px;font-size:32px}.world-intro p{font-size:13px;line-height:1.6}.hero-status{padding:14px}.interaction-guide{display:grid;gap:8px;padding:12px;font-size:9px}.world-map{grid-template-columns:1fr;margin-top:12px;padding:58px 12px 16px}.world-core,.node-bottom,.growth-axis{grid-column:auto}.world-tree-view{display:none}.product-section{padding:62px 20px}.status-grid,.automation-grid,.governance-grid,.architecture-grid,.registry-grid{grid-template-columns:1fr}.six-w{grid-template-columns:1fr}.system-card,.capability-card,.info-card,.metadata-card{padding:20px}.flow,.hierarchy{justify-content:flex-start}.product-footer{padding:24px 20px}.platform-intro{padding:86px 20px 24px}[data-testid="stAppViewContainer"]:has(.integrated-platform) .block-container{padding:0 14px 56px!important}.platform-landmark{left:20px;top:24px}}@media(prefers-reduced-motion:reduce){*{transition:none!important;scroll-behavior:auto!important}}
    </style>""")


def render_ai_hub() -> None:
    """Render AI Hub inside the shared OS Ecosystem product shell."""
    source = str(AI_HUB_SOURCE)
    if source not in sys.path:
        sys.path.insert(0, source)
    from ai_hub.presentation.operator_ui.app import build_initial_snapshot
    from ai_hub.presentation.operator_ui.pages.dashboard import render_dashboard
    st.html(f'<main class="integrated-platform">{_product_header_markup("AI Hub")}<section class="platform-intro"><span class="platform-landmark" aria-hidden="true"></span><span class="eyebrow">내부 성장 시스템 · AI 운영</span><h1>AI Hub</h1><p>씨앗에서 성장하는 내부 시스템으로서 AI 제공자 상태, 라우팅과 안전한 실행 기록을 OS Ecosystem 안에서 확인합니다.</p></section></main>')
    render_dashboard(build_initial_snapshot(), st)


def main() -> None:
    st.set_page_config(page_title="OS Ecosystem", page_icon="◈", layout="wide", initial_sidebar_state="collapsed")
    apply_theme()
    if st.query_params.get("project") == "ai-hub":
        render_ai_hub()
        return
    render_launcher(get_projects())


if __name__ == "__main__":
    main()
