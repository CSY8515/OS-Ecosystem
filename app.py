"""OS Ecosystem v0.7.1 concept-as-interface preview."""

from __future__ import annotations

import base64
import html
import os
import sys
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from urllib.parse import urlparse

import streamlit as st


VERSION = "0.7.1"
AI_HUB_SOURCE = Path(__file__).resolve().parent / "AI-Hub" / "src"
ASSET_ROOT = Path(__file__).resolve().parent / "assets"
KEY_VISUAL_PATH = ASSET_ROOT / "os-ecosystem-official-answer-v071-final-key-visual.png"
PROJECT_SEED_ART = {
    "Living OS": ASSET_ROOT / "project-seeds" / "living-os-official-v071-final.png",
    "Universal Learning Engine": ASSET_ROOT / "project-seeds" / "universal-learning-engine-official-v071-final.png",
    "AI Hub": ASSET_ROOT / "project-seeds" / "ai-hub-official-v071-final.png",
}


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


@lru_cache(maxsize=8)
def _asset_data_uri(path: Path) -> str:
    """Return a project-owned PNG as an inline deployment-safe asset."""
    encoded = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:image/png;base64,{encoded}"


def _key_visual_data_uri() -> str:
    return _asset_data_uri(KEY_VISUAL_PATH)


def get_projects() -> tuple[Project, ...]:
    """Return public and repository-owned OS Systems."""
    return (
        Project(
            "Living OS",
            "실생활 운영",
            "일상 기록과 생활 기능을 한 흐름으로 관리합니다.",
            _configured_url(
                "LIVING_OS_URL",
                "https://living-os-h5uinmvmjpvv6m8phat28a.streamlit.app/",
            ),
            "node-living",
        ),
        Project(
            "Universal Learning Engine",
            "범용 학습 엔진",
            "어떤 주제든 구조화된 학습 경험으로 연결합니다.",
            _configured_url(
                "ULE_URL",
                "https://universal-learning-engine-zb5aezuadeu84gnqust8mw.streamlit.app/",
            ),
            "node-learning",
        ),
        Project(
            "AI Hub",
            "AI 운영",
            "승인된 AI 연결과 실행 상태를 안전하게 확인합니다.",
            "?project=ai-hub",
            "node-ai",
        ),
    )


def get_project_metadata(project: Project) -> SixWMetadata:
    known = {
        "Living OS": SixWMetadata(
            "개인 사용자와 Living OS",
            "생활 기능이 필요할 때",
            "독립된 Living OS",
            "실생활 운영",
            "공개 HTTPS 화면으로 직접 연결",
            "생활 기록과 운영을 지속적으로 관리",
        ),
        "Universal Learning Engine": SixWMetadata(
            "학습자와 Universal Learning Engine",
            "새로운 학습이 필요할 때",
            "독립된 Universal Learning Engine",
            "주제별 범용 학습",
            "공개 HTTPS 화면으로 직접 연결",
            "반복 가능한 학습 경험 제공",
        ),
        "AI Hub": SixWMetadata(
            "승인된 사용자와 연결 프로젝트",
            "AI 상태와 경로를 확인할 때",
            "OS Ecosystem 내부",
            "AI 연결과 운영",
            "정책 기반 선택과 안전한 기록",
            "AI 사용을 한곳에서 통제하고 설명",
        ),
    }
    return known.get(
        project.name,
        SixWMetadata(
            "승인된 사용자",
            "필요할 때",
            "등록된 시스템",
            project.description,
            "승인된 경로로 연결",
            "등록 목적을 수행",
        ),
    )


def get_capabilities() -> tuple[Capability, ...]:
    when, where = "공통 기능이 호출될 때", "OS Ecosystem Core"
    return (
        Capability(
            "Safety Capability",
            "안전",
            "v1.0.0",
            "안정",
            "실행 전에 위험을 확인하고 실패를 격리합니다.",
            "cap-safety",
            ("검증", "실행", "상태 확인"),
            SixWMetadata("모든 연결 시스템", when, where, "공통 안전 실행", "검증과 격리", "위험한 실행 통제"),
        ),
        Capability(
            "Enhancement Capability",
            "향상",
            "v1.0.0",
            "안정",
            "분석과 학습을 통해 개선 근거를 제공합니다.",
            "cap-enhancement",
            ("분석", "학습", "패턴", "지식", "최적화", "규칙"),
            SixWMetadata("개선이 필요한 프로젝트", when, where, "분석과 개선", "요청·결과 계약", "지속적인 개선 근거 제공"),
        ),
        Capability(
            "Automation Capability",
            "자동화",
            "v1.0.0",
            "안정",
            "승인과 안전 확인을 통과한 반복 작업을 실행합니다.",
            "automation",
            ("작업 흐름", "일정", "조건", "반복", "자동 실행", "결정 지원"),
            SixWMetadata("승인된 사용자와 프로젝트", when, where, "반복 작업 실행", "검증→승인→실행→기록", "반복 작업의 안전한 수행"),
        ),
        Capability(
            "Collaboration & Connectivity",
            "연결",
            "v1.0.0",
            "데모",
            "독립 시스템 사이의 교환과 동기화 경로를 제공합니다.",
            "connectivity",
            ("연결 목록", "교환", "메시지", "동기화", "상태"),
            SixWMetadata("연결이 승인된 시스템", when, where, "연결과 교환", "연결 어댑터와 안전 계약", "시스템 간 결합 완화"),
        ),
        Capability(
            "Personal Secretary Capability",
            "개인 비서",
            "v1.0.0",
            "안정",
            "브리핑, 알림, 추천과 다음 행동을 이해하기 쉽게 제안합니다.",
            "secretary",
            ("브리핑", "검토", "알림", "추천", "우선순위", "결정"),
            SixWMetadata("사용자와 호출 프로젝트", when, where, "요약과 결정 지원", "종합과 안전 확인", "다음 행동을 명확히 제안"),
        ),
    )


def _six_w_markup(metadata: SixWMetadata) -> str:
    fields = (
        ("누가", "Who", metadata.who),
        ("언제", "When", metadata.when),
        ("어디서", "Where", metadata.where),
        ("무엇을", "What", metadata.what),
        ("어떻게", "How", metadata.how),
        ("왜", "Why", metadata.why),
    )
    return '<dl class="six-w">' + "".join(
        f'<div><dt>{ko}<small>{en}</small></dt><dd>{html.escape(value)}</dd></div>'
        for ko, en, value in fields
    ) + "</dl>"


def _icon_svg(kind: str) -> str:
    icons = {
        "fruit": '<svg viewBox="0 0 48 48" aria-hidden="true"><path d="M25 10c9 0 15 7 14 16-1 10-7 17-15 17S10 35 10 26c0-8 6-16 15-16Z"/><path d="M25 11c2-5 6-7 11-7-1 5-4 8-11 7Z"/></svg>',
        "seed": '<svg viewBox="0 0 48 48" aria-hidden="true"><path d="M25 5c10 9 14 17 12 25-2 8-7 13-14 13S11 38 11 30c0-9 5-17 14-25Z"/><path d="M25 16v18M25 25l-7-5M25 29l7-6"/></svg>',
        "sapling": '<svg viewBox="0 0 64 64" aria-hidden="true"><path d="M32 58V28M32 38 20 28M32 44l13-12"/><path d="M17 31c-7-1-11-7-9-13 2-6 9-9 15-6 3-7 13-9 19-4 7 0 12 6 11 13 5 4 4 12-1 16-5 4-12 3-16-2-5 4-13 3-19-4Z"/><path d="M20 58h24M32 58l-8 4M32 58l8 4"/></svg>',
        "core": '<svg viewBox="0 0 64 64" aria-hidden="true"><path d="M32 55V25M32 30 18 18M32 37l15-15M32 25V9"/><path d="M12 22c0-8 6-14 14-14 2-5 8-7 13-4 7-2 14 4 13 12 6 3 7 12 2 17-4 5-12 4-16 0-5 5-14 5-18-1-6 1-11-4-10-10Z"/><path d="M32 54 19 61M32 54l13 7"/></svg>',
        "shield": '<svg viewBox="0 0 48 48" aria-hidden="true"><path d="M24 5 39 11v11c0 10-6 17-15 21C15 39 9 32 9 22V11l15-6Z"/><path d="m17 24 5 5 10-12"/></svg>',
        "growth": '<svg viewBox="0 0 48 48" aria-hidden="true"><path d="M8 39h32M13 34l8-9 6 5 9-14"/><path d="M29 16h7v7"/></svg>',
        "automation": '<svg viewBox="0 0 48 48" aria-hidden="true"><path d="M13 13h9v9h-9zM26 26h9v9h-9zM31 13h6v6M17 29h-6v6"/><path d="M22 17h9M17 22v7M31 19v7M17 35h9"/></svg>',
        "connection": '<svg viewBox="0 0 48 48" aria-hidden="true"><circle cx="13" cy="24" r="6"/><circle cx="35" cy="13" r="6"/><circle cx="35" cy="35" r="6"/><path d="m18 21 11-5M18 27l11 5"/></svg>',
        "guide": '<svg viewBox="0 0 48 48" aria-hidden="true"><circle cx="24" cy="16" r="8"/><path d="M11 41c1-10 6-16 13-16s12 6 13 16M24 25v16"/></svg>',
        "rules": '<svg viewBox="0 0 48 48" aria-hidden="true"><path d="M12 7h24v34H12zM18 15h12M18 22h12M18 29h8"/></svg>',
        "structure": '<svg viewBox="0 0 48 48" aria-hidden="true"><path d="M18 7h12v9H18zM7 32h12v9H7zM29 32h12v9H29zM24 16v8M13 24h22M13 24v8M35 24v8"/></svg>',
        "record": '<svg viewBox="0 0 48 48" aria-hidden="true"><path d="M9 9h30v30H9zM15 16h18M15 24h18M15 32h11"/></svg>',
    }
    return icons[kind]


def _project_node(project: Project) -> str:
    name = html.escape(project.name)
    label = html.escape(project.label)
    seed_art = _asset_data_uri(PROJECT_SEED_ART.get(project.name, PROJECT_SEED_ART["Living OS"]))
    if not project.url:
        return (
            f'<div class="project-seed {project.position} is-unavailable" aria-disabled="true" '
            f'aria-label="{name} 프로젝트 씨앗, 연결 준비 중">'
            f'<img class="mobile-seed-art" src="{seed_art}" alt="" aria-hidden="true">'
            f'<span class="project-seed-label"><strong>{name}</strong>'
            f'<em>{label}</em><b aria-hidden="true">준비 중</b></span></div>'
        )
    external = project.url.startswith(("http://", "https://"))
    rendered_url = project.url if external or not project.url.startswith("?") else f"./{project.url}"
    url = html.escape(rendered_url, quote=True)
    attrs = 'target="_blank" rel="noopener noreferrer"' if external else 'target="_self" rel="noopener noreferrer"'
    route = "새 탭에서 열기" if external else "현재 화면에서 열기"
    route_icon = "↗" if external else "→"
    return (
        f'<a class="project-seed {project.position} is-action world-action" '
        f'href="{url}" {attrs} aria-label="{name} 프로젝트 씨앗, {route}">'
        f'<img class="mobile-seed-art" src="{seed_art}" alt="" aria-hidden="true" loading="lazy">'
        f'<span class="project-seed-label"><strong>{name}</strong>'
        f'<em>{label}</em><b aria-hidden="true">{route_icon}</b></span></a>'
    )


def _capability_node(item: Capability, position: str, icon: str) -> str:
    modules = " · ".join(item.modules[:3])
    return (
        f'<a class="map-node seed-node {position} is-action world-action" href="#{item.anchor}" target="_self" '
        f'aria-label="{item.korean_name} 기능 자세히 보기">'
        f'<span class="seed-dome"><span class="node-icon">{_icon_svg(icon)}</span></span><span class="node-copy">'
        f'<small>돔형 씨앗 · {html.escape(modules)}</small><strong>{html.escape(item.korean_name)}</strong>'
        f'<span>{html.escape(item.description)}</span><b>기능 보기 <i aria-hidden="true">↓</i></b>'
        f'<em class="technical-term">{html.escape(item.name)}</em></span></a>'
    )


def _orientation_markup(current: str) -> str:
    current_label = {
        "AI Hub": "AI Hub · AI 운영",
        "Overview": "OS Ecosystem · 전체 보기",
    }.get(current, "OS Ecosystem · 생태계 중심")
    current_attr = ' aria-current="page"' if current == "Home" else ""
    return f'''
    <header class="orientation-bar">
      <div class="brand-lockup">
        <a href="./" target="_self" class="brand-home" aria-label="OS Ecosystem 홈으로 이동">
          <span class="brand-mark" aria-hidden="true">{_icon_svg("core")}</span>
          <span><strong>OS Ecosystem</strong><small>CONNECTED WORLD SYSTEM</small></span>
        </a>
        <span class="version-state">v{VERSION} · 안정 버전</span>
      </div>
      <nav class="location-path breadcrumb" aria-label="현재 위치">
        <span>현재 위치</span><strong>{current_label}</strong>
      </nav>
      <a class="home-return" href="./" target="_self"{current_attr} aria-label="홈으로 돌아가기">
        <span aria-hidden="true">⌂</span><b>홈</b><small>돌아가기</small>
      </a>
    </header>'''


def _product_header_markup(current: str) -> str:
    """Backward-compatible name for the shared orientation component."""
    return _orientation_markup(current)


def _project_metadata_disclosure(projects: tuple[Project, ...]) -> str:
    sections = "".join(
        f'<section><h3>{html.escape(project.name)}</h3>{_six_w_markup(get_project_metadata(project))}</section>'
        for project in projects
    )
    return (
        '<details class="context-drawer"><summary>연결 이유와 책임 확인'
        '<small>6하 원칙 설명</small></summary><div class="context-columns">'
        f'{sections}</div></details>'
    )


def _capability_field(item: Capability) -> str:
    modules = "".join(f'<li>{html.escape(module)}</li>' for module in item.modules)
    return f'''
    <section class="field-row capability-field" id="{item.anchor}" tabindex="-1">
      <div class="field-index"><span>{item.status} · {item.version}</span><small>{item.name}</small></div>
      <div class="field-copy"><h3>{item.korean_name}</h3><p>{item.description}</p><ul>{modules}</ul></div>
      <details><summary>6하 원칙 보기</summary>{_six_w_markup(item.metadata)}</details>
    </section>'''


def _render_launcher_prototype(projects: tuple[Project, ...]) -> None:
    project_nodes = "".join(_project_node(project) for project in projects)
    capabilities = get_capabilities()
    positions = ("seed-safety", "seed-growth", "seed-automation", "seed-connection", "seed-guide")
    icons = ("shield", "growth", "automation", "connection", "guide")
    capability_nodes = "".join(
        _capability_node(item, position, icon)
        for item, position, icon in zip(capabilities, positions, icons)
    )
    capability_fields = "".join(_capability_field(item) for item in capabilities)
    core_metadata = _six_w_markup(
        SixWMetadata(
            "OS Ecosystem 사용자와 운영자",
            "연결된 시스템을 탐색할 때",
            "현재 저장소와 Streamlit 앱",
            "통합 탐색과 운영 기준",
            "공개 경로·설명·시스템 정보",
            "독립 시스템을 일관되게 연결",
        )
    )
    st.markdown(f'''
    <main class="ecosystem-shell">
      {_orientation_markup("Home")}
      <section class="atlas-stage" id="projects" aria-labelledby="atlas-title">
        <div class="atlas-heading">
          <span>OS ECOSYSTEM 열매 내부</span>
          <h1 id="atlas-title">세계수에서 탐색하세요.</h1>
          <p>묘목은 프로젝트로, 돔형 씨앗은 기능으로 이어집니다. 이름과 이동 방식을 확인한 뒤 세계로 들어가세요.</p>
        </div>
        <div class="atlas-status" role="status"><i aria-hidden="true"></i><span>정상 운영</span><small>OS Ecosystem v{VERSION}</small></div>
        <ol class="cosmic-lineage" aria-label="공식 세계 계층">
          <li><small>우주</small><b>Universe</b></li>
          <li><small>거대한 세계수</small><b>Ultra Brain</b></li>
          <li><small>거대한 가지</small><b>Meta OS</b></li>
          <li aria-current="location"><small>현재 열매</small><b>OS Ecosystem</b></li>
        </ol>
        <div class="world-atlas" aria-label="OS Ecosystem 세계 탐색 지도">
          <img class="ecosystem-key-visual" src="{_key_visual_data_uri()}" alt="" aria-hidden="true" decoding="async" fetchpriority="high">
          <div class="fruit-universe world-landmark" aria-label="Meta OS 가지에 열린 OS Ecosystem 열매 내부">
            <span class="fruit-stem" aria-hidden="true"></span>
            <span class="fruit-boundary-label">META OS 가지에서 들어온 열매 내부</span>
          </div>
          <div class="mobile-layer layer-core"><span>세계수</span><b>현재 탐색 중심</b></div>
          <div class="mobile-layer layer-projects"><span>묘목</span><b>연결된 프로젝트</b></div>
          <div class="mobile-layer layer-seeds"><span>돔형 씨앗</span><b>기능과 엔진</b></div>
          <div class="mobile-layer layer-roots"><span>뿌리</span><b>운영 기반</b></div>
          <svg class="ecosystem-tree" viewBox="0 0 900 620" role="img" aria-label="OS Ecosystem Core와 연결된 세계수">
            <path class="canopy-mass" d="M450 66c-76-35-149 2-174 63-74-1-123 53-107 119-55 47-25 139 47 149 19 63 100 82 151 43 50 52 151 43 178-22 79 1 124-80 84-141 35-62-17-140-88-143-9-68-47-123-91-88Z"/>
            <path class="trunk-mass" d="M415 488c22-74 24-152 35-235 13 85 15 163 39 235l-39 35Z"/>
            <path class="branch-line project-branch" d="M448 305 239 185M452 303l210-119M462 352l202 97"/>
            <path class="branch-line seed-branch" d="M438 350 242 375M431 405 285 490M470 405l145 84M462 352l195 29M450 480v70"/>
            <path class="root-line" d="M450 483 291 574M450 483l164 91M450 490v113M450 520 360 610M450 520l91 90"/>
          </svg>
          <div class="core-landmark world-landmark is-selected" aria-current="location" aria-label="현재 위치 OS Ecosystem Core">
            <span class="node-icon">{_icon_svg("core")}</span>
            <span class="node-copy"><small>현재 위치 · Navigation Hub</small><strong>OS Ecosystem</strong><span>열매 안의 세계수</span></span>
          </div>
          {project_nodes}
          <div class="seed-garden" id="capability" aria-label="공통 기능 돔형 씨앗">
            {capability_nodes}
          </div>
          <nav class="root-foundation" aria-label="OS Ecosystem 운영 기반">
            <a class="map-node root-node root-governance is-action world-action" href="#governance" target="_self" aria-label="운영 기준 보기">
              <span class="node-icon">{_icon_svg("rules")}</span><span class="node-copy"><small>책임과 원칙</small><strong>운영 기준</strong><b>확인하기 <i aria-hidden="true">↓</i></b><em class="technical-term">Governance</em></span>
            </a>
            <a class="map-node root-node root-architecture is-action world-action" href="#architecture" target="_self" aria-label="시스템 구조 보기">
              <span class="node-icon">{_icon_svg("structure")}</span><span class="node-copy"><small>계층과 연결</small><strong>시스템 구조</strong><b>확인하기 <i aria-hidden="true">↓</i></b><em class="technical-term">Architecture</em></span>
            </a>
            <a class="map-node root-node root-registry is-action world-action" href="#registry" target="_self" aria-label="시스템 정보 보기">
              <span class="node-icon">{_icon_svg("record")}</span><span class="node-copy"><small>버전과 상태</small><strong>시스템 정보</strong><b>확인하기 <i aria-hidden="true">↓</i></b><em class="technical-term">Registry</em></span>
            </a>
          </nav>
        </div>
        {_project_metadata_disclosure(projects)}
      </section>

      <section class="field-zone" id="ai-hub">
        <header><span>묘목 · 내부 프로젝트</span><h2>AI Hub</h2><p>OS Ecosystem 안에서 자라는 독립된 프로젝트 묘목이며, 승인된 AI 연결과 운영 상태를 관리합니다.</p></header>
        <div class="field-line"><span>구성요소</span><strong>v0.1.0 · 통합</strong><span>연결 방식</span><strong>정책 기반 자동 선택</strong><span>지원 범위</span><strong>OpenAI · Gemini · Claude</strong></div>
        <a class="field-action" href="./?project=ai-hub" target="_self">AI 운영 화면 열기 <span aria-hidden="true">→</span></a>
      </section>

      <section class="field-zone" aria-labelledby="functions-title">
        <header><span>돔형 씨앗 · 성장 기능</span><h2 id="functions-title">공통 기능</h2><p>Subsystem, Module, Capability, Engine은 세계수 안에서 성장하는 씨앗으로 관리합니다.</p></header>
        <div class="field-stream">{capability_fields}</div>
      </section>

      <section class="field-zone" id="governance" tabindex="-1">
        <header><span>뿌리 · 책임 경계</span><h2>운영 기준</h2><p>Ultra Brain 전용 Governance를 해석하거나 대체하지 않고 OS Ecosystem 운영 책임만 관리합니다.</p></header>
        <div class="boundary-line"><strong>OS Ecosystem</strong><span>연결 · 등록 · 호환성 · 검증 · 릴리스</span><strong>Ultra Brain</strong><span>전용 최상위 Governance · 본 제품 범위 밖</span></div>
        <div class="plain-list"><p><b>헌장</b><span>권한, 프로젝트 자율성과 소유권 경계를 정의합니다.</span></p><p><b>규칙</b><span>연결, 승인된 변경과 릴리스 책임을 관리합니다.</span></p><p><b>원칙</b><span>현재 PRINCIPLES.md 원문을 유지하며 별도 6대 운영 원칙은 공식 문서 확인 후 반영합니다.</span></p><p><b>표준과 정책</b><span>호환성, 문서, 테스트, 보안과 공개 기준을 기록합니다.</span></p></div>
      </section>

      <section class="field-zone" id="architecture" tabindex="-1">
        <header><span>뿌리 · 연결 구조</span><h2>시스템 구조</h2><p>소유권과 배포 경계를 유지하면서 각 계층이 바로 아래 계층만 관리합니다.</p></header>
        <div class="hierarchy-line"><span>Universe</span><i>→</i><span>Ultra Brain</span><i>→</i><span>Meta OS</span><i>→</i><span>OS Ecosystem</span><i>→</i><span>Project</span><i>→</i><span>Subsystem</span><i>→</i><span>Module</span><i>→</i><span>Capability</span><i>→</i><span>Engine</span></div>
        <div class="plain-list"><p><b>전체 구조</b><span>독립 프로젝트를 연결하는 탐색·운영 계층입니다.</span></p><p><b>저장소</b><span>독립 프로젝트는 독립 저장소를 유지하고 AI Hub는 현재 저장소에 남습니다.</span></p><p><b>통합</b><span>독립 프로젝트는 직접 링크, AI Hub는 내부 경로를 사용합니다.</span></p><p><b>6하 원칙</b><span>설명과 추적성의 공통 기준으로 사용합니다.</span></p></div>
      </section>

      <section class="field-zone" id="registry" tabindex="-1">
        <header><span>뿌리 · 기록과 추적</span><h2>시스템 정보</h2><p>사용자에게 필요한 브랜드, 버전, 연결 상태와 릴리스 정보만 표시합니다.</p></header>
        <div class="registry-lines">
          <p><span>OS Ecosystem</span><b>v{VERSION} · 안정 버전</b></p><p><span>AI Hub</span><b>v0.1.0 · 내부 통합</b></p><p><span>Living OS</span><b>v2.0.4 · 외부 연결</b></p><p><span>Universal Learning Engine</span><b>v1.0.0 · 외부 연결</b></p>
        </div>
        <details class="technical-disclosure"><summary>개발 정보 보기</summary><p>Project Registry · Capability Registry · Contract Registry · Route Registry는 기존 문서 구조와 책임 경계를 그대로 유지합니다.</p></details>
      </section>

      <section class="core-context" id="core-context"><h2>OS Ecosystem Core 설명</h2>{core_metadata}</section>
      <footer class="product-footer"><span>OS Ecosystem</span><span>연결된 시스템을 하나의 세계에서 탐색합니다.</span></footer>
    </main>''', unsafe_allow_html=True)


def render_launcher(projects: tuple[Project, ...]) -> None:
    """Render the official fruit-interior world with Project Seeds only."""
    project_seeds = "".join(_project_node(project) for project in projects)
    st.markdown(f'''
    <main class="ecosystem-shell official-world-shell">
      {_orientation_markup("Home")}
      <section class="official-world" id="projects" aria-labelledby="official-world-title">
        <h1 class="sr-only" id="official-world-title">OS Ecosystem</h1>
        <div class="world-stage" aria-label="OS Ecosystem 열매 안의 우주와 세 개의 프로젝트 씨앗">
          <img class="ecosystem-key-visual" src="{_key_visual_data_uri()}" alt="" aria-hidden="true" decoding="async" fetchpriority="high">
          <a class="core-signature core-action is-selected" href="./?view=overview" target="_self" rel="noopener noreferrer"
             aria-current="location" aria-label="OS Ecosystem Overview 현재 화면에서 열기">
            <strong>OS Ecosystem</strong>
            <span class="core-action-hint">전체 보기 <b aria-hidden="true">→</b></span>
          </a>
          <nav class="project-seed-field" aria-label="프로젝트 씨앗">
            {project_seeds}
          </nav>
        </div>
      </section>
    </main>''', unsafe_allow_html=True)


def apply_theme() -> None:
    st.html('''<style>
    :root{--font-ui:-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;--space:#0f2028;--space-2:#142b33;--forest:#203c35;--forest-2:#29493e;--bark:#514b38;--earth:#353126;--paper:#f3f0e6;--paper-soft:#cbd3cc;--muted:#93a7a5;--line:#67827f;--line-soft:rgba(187,211,203,.22);--leaf:#9ebd79;--fruit:#ca9d62;--seed:#d7bb78;--water:#7fadb5;--danger:#d28b78}
    html,body,[data-testid="stAppViewContainer"]{background:var(--space);color:var(--paper);overflow-x:hidden}[data-testid="stHeader"],[data-testid="stSidebar"],[data-testid="stToolbar"],footer{display:none!important}.stApp{background:var(--space);font-family:var(--font-ui)}.block-container{max-width:none;padding:0!important}.ecosystem-shell{min-height:100vh}.ecosystem-shell,.integrated-platform{color:var(--paper);font-family:var(--font-ui)}
    .ecosystem-shell h1>a,.ecosystem-shell h2>a,.ecosystem-shell h3>a,.integrated-platform h1>a,.integrated-platform h2>a,.integrated-platform h3>a{display:none!important}
    .orientation-bar{position:sticky;top:0;z-index:30;display:grid;grid-template-columns:1fr auto auto;align-items:center;gap:24px;min-height:68px;padding:0 clamp(18px,3.5vw,54px);border-bottom:1px solid var(--line-soft);background:var(--space)}.brand-lockup,.brand-home,.location-path,.home-return{display:flex;align-items:center}.brand-lockup{gap:18px}.brand-home{gap:11px;color:var(--paper)!important;text-decoration:none!important}.brand-mark{width:34px;height:34px}.brand-mark svg{width:100%;height:100%;fill:none;stroke:var(--leaf);stroke-width:2}.brand-home strong{display:block;font-size:14px;letter-spacing:.05em}.brand-home small{display:block;margin-top:2px;color:var(--muted);font-size:7px;letter-spacing:.18em}.version-state{padding-left:16px;border-left:1px solid var(--line-soft);color:var(--seed);font-size:9px}.location-path{gap:10px}.location-path span{color:var(--muted);font-size:9px}.location-path strong{font-size:11px;font-weight:600}.home-return{gap:7px;min-height:44px;padding:0 13px;border:1px solid var(--line);color:var(--paper)!important;text-decoration:none!important;transition:border-color .16s ease,background .16s ease}.home-return>span{color:var(--leaf);font-size:18px}.home-return b{font-size:11px}.home-return small{color:var(--muted);font-size:8px}.home-return:hover,.home-return:focus-visible{border-color:var(--paper);background:#1b343b;outline:3px solid rgba(244,240,228,.18);outline-offset:2px}
    .atlas-stage{position:relative;min-height:calc(100vh - 68px);background:var(--space);overflow:hidden}.atlas-stage:after{content:"";position:absolute;z-index:2;inset:0;pointer-events:none;background:linear-gradient(90deg,rgba(7,18,22,.68) 0%,transparent 34%,transparent 70%,rgba(7,18,22,.3) 100%)}.atlas-heading{position:absolute;z-index:9;left:clamp(18px,3.5vw,54px);top:22px;max-width:480px;text-shadow:0 2px 7px rgba(0,0,0,.9)}.atlas-heading>span{color:#d8bd7d;font-size:9px;letter-spacing:.18em}.atlas-heading h1{margin:7px 0 6px;font-size:clamp(26px,2.6vw,38px);line-height:1.08;letter-spacing:-.035em}.atlas-heading p{margin:0;color:#e1e3dc;font-size:11px;line-height:1.55}.atlas-status{position:absolute;z-index:9;right:clamp(18px,3.5vw,54px);top:28px;display:grid;grid-template-columns:auto auto;gap:2px 8px;align-items:center;text-shadow:0 2px 7px rgba(0,0,0,.9)}.atlas-status i{grid-row:1/3;width:8px;height:8px;border-radius:50%;background:var(--leaf)}.atlas-status span{font-size:10px}.atlas-status small{color:var(--paper-soft);font-size:8px}
    .cosmic-lineage{position:absolute;z-index:8;right:clamp(18px,3.5vw,54px);top:108px;display:grid;grid-template-columns:repeat(4,minmax(110px,1fr));width:min(650px,54vw);margin:0;padding:0;list-style:none}.cosmic-lineage li{position:relative;padding:0 16px;text-align:center}.cosmic-lineage li:not(:last-child):after{content:"→";position:absolute;right:-5px;top:10px;color:var(--line);font-size:11px}.cosmic-lineage small,.cosmic-lineage b{display:block}.cosmic-lineage small{color:var(--muted);font-size:7px}.cosmic-lineage b{margin-top:3px;color:var(--paper-soft);font-size:9px;font-weight:500}.cosmic-lineage li[aria-current="location"] b{color:var(--seed);font-weight:700}.cosmic-lineage li[aria-current="location"]:before{content:"";position:absolute;left:50%;bottom:-8px;width:24px;height:2px;background:var(--seed);transform:translateX(-50%)}
    .world-atlas{position:relative;height:calc(100vh - 68px);min-height:640px;max-width:1664px;margin:0 auto;background:#0d1b20}.ecosystem-key-visual{position:absolute;z-index:0;inset:0;width:100%;height:100%;object-fit:cover;object-position:center center}.fruit-universe{position:absolute;z-index:4;inset:0;pointer-events:none}.fruit-stem{display:none}.fruit-boundary-label{position:absolute;left:50%;top:153px;padding:5px 12px;border-top:1px solid rgba(216,189,125,.45);border-bottom:1px solid rgba(216,189,125,.45);background:rgba(8,20,24,.72);color:#d4c19a;font-size:7px;letter-spacing:.12em;transform:translateX(-50%);white-space:nowrap;text-shadow:0 2px 6px #000}
    .ecosystem-tree{display:none}.mobile-layer{display:none}
    .map-node,.core-landmark{z-index:5;color:var(--paper);text-decoration:none;text-shadow:0 2px 6px #000}.map-node{box-sizing:border-box}.node-icon{display:grid;place-items:center}.node-icon svg,.sapling-emblem svg,.subsystem-seeds svg{width:100%;height:100%;fill:none;stroke:currentColor;stroke-width:1.8;stroke-linecap:round;stroke-linejoin:round}.node-copy{display:block;min-width:0}.node-copy small,.node-copy strong,.node-copy span,.node-copy b,.node-copy em{display:block}.node-copy small{color:#e4e1d5;font-size:8px;letter-spacing:.04em}.node-copy strong{margin:3px 0;color:#fff;font-size:16px;line-height:1.15}.node-copy span{max-width:210px;color:#d5ddd8;font-size:9px;line-height:1.35}.node-copy b{margin-top:6px;color:#f0ca7c;font-size:9px;font-weight:700}.node-copy b i{font-style:normal}.technical-term{margin-top:3px;color:#b3c2bd;font-size:7px;font-style:normal;letter-spacing:.08em}.world-action{cursor:pointer;transition:border-color .16s ease,color .16s ease,transform .16s ease,background .16s ease}.world-action:hover,.world-action:focus-visible{outline:3px solid rgba(244,240,228,.28);outline-offset:3px}.world-action:hover{transform:translateY(-2px)}.is-unavailable{opacity:.62}
    .project-node{position:absolute;display:grid;grid-template-columns:70px minmax(160px,1fr);align-items:center;gap:10px;width:min(292px,24vw);min-height:104px;padding:8px 12px;border-left:2px solid var(--project);border-bottom:1px solid color-mix(in srgb,var(--project) 55%,transparent);background:rgba(7,18,22,.72);--project:var(--leaf)}.sapling-figure{position:relative;display:grid;place-items:center;width:66px;height:78px;color:var(--project)}.sapling-figure .node-icon{z-index:2;width:48px;height:58px}.sapling-orbit{position:absolute;inset:3px 0 8px;border:1px solid color-mix(in srgb,var(--project) 75%,transparent);border-radius:50%;transition:border-color .16s ease,transform .16s ease}.project-node:hover .sapling-orbit,.project-node:focus-visible .sapling-orbit{border-color:var(--paper);transform:rotate(9deg)}.node-living{left:3%;top:46%;--project:#b4c483}.node-learning{right:3%;top:39%;--project:#8bbbc1}.node-ai{right:4%;top:62%;--project:#d3ad69}
    .core-landmark{position:absolute;left:50%;top:44%;display:flex;align-items:center;flex-direction:column;padding:8px 18px;text-align:center;transform:translate(-50%,-50%);background:rgba(7,18,22,.54);border-bottom:1px solid rgba(158,189,121,.72)}.core-landmark .node-icon{width:78px;height:78px;color:#bfd38d}.core-landmark .node-copy strong{font-size:20px}.core-landmark .node-copy small{color:#d5e6ab}.core-landmark.is-selected:after{content:"현재 위치";margin-top:7px;padding:3px 9px;border:1px solid var(--leaf);border-radius:999px;color:var(--paper);font-size:8px}
    .seed-garden{position:absolute;z-index:6;left:15%;right:15%;bottom:92px;display:grid;grid-template-columns:repeat(5,minmax(92px,1fr));gap:22px;align-items:end}.seed-node{position:relative;display:flex;align-items:center;flex-direction:column;min-width:0;min-height:112px;padding:0 4px;text-align:center}.seed-dome{display:grid;place-items:center;width:74px;height:58px;border:1px solid rgba(225,196,126,.9);border-bottom:4px solid #9f8755;border-radius:50% 50% 14% 14%/72% 72% 18% 18%;background:rgba(8,20,24,.7);color:#efd18a;transition:border-color .16s ease,background .16s ease,transform .16s ease}.seed-dome .node-icon{width:30px;height:30px}.seed-node .node-copy small{max-width:106px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}.seed-node .node-copy strong{font-size:13px}.seed-node .node-copy>span,.seed-node .technical-term{display:none}.seed-node:hover .seed-dome,.seed-node:focus-visible .seed-dome{border-color:var(--paper);background:rgba(31,57,48,.88);transform:translateY(-3px)}
    .root-foundation{position:absolute;z-index:7;left:4%;right:4%;bottom:8px;display:flex;align-items:end;justify-content:space-between}.root-node{position:relative;display:flex;align-items:center;gap:10px;width:220px;min-height:56px;padding:5px 9px;border-top:1px solid var(--water);background:rgba(7,18,22,.7)}.root-node .node-icon{flex:0 0 36px;width:36px;height:36px;color:#9cc1c6}.root-node:hover,.root-node:focus-visible{border-color:var(--paper);background:rgba(23,46,52,.9)}
    .context-drawer{position:relative;z-index:8;max-width:1220px;margin:0 auto;border-top:1px solid var(--line);background:#142a31}.context-drawer summary{box-sizing:border-box;min-height:52px;padding:16px 18px;color:var(--paper);cursor:pointer;font-size:11px;list-style:none}.context-drawer summary::-webkit-details-marker{display:none}.context-drawer summary:after{content:"＋";float:right;color:var(--seed)}.context-drawer[open] summary:after{content:"−"}.context-drawer summary small{margin-left:10px;color:var(--muted);font-size:8px}.context-columns{display:grid;grid-template-columns:repeat(3,1fr);border-top:1px solid var(--line-soft)}.context-columns>section{padding:18px;border-right:1px solid var(--line-soft)}.context-columns>section:last-child{border-right:0}.context-columns h3{margin:0 0 12px;font-size:14px}
    .field-zone,.core-context{max-width:1180px;margin:0 auto;padding:76px clamp(20px,4vw,54px);border-top:1px solid var(--line-soft);scroll-margin-top:80px}.field-zone>header{display:grid;grid-template-columns:minmax(240px,.65fr) 1.35fr;gap:32px;align-items:end;margin-bottom:28px}.field-zone>header>span{grid-column:1;color:var(--seed);font-size:9px;letter-spacing:.15em}.field-zone>header h2{grid-column:1;margin:4px 0 0;font-size:34px;letter-spacing:-.03em}.field-zone>header p{grid-column:2;grid-row:1/3;margin:0;color:var(--paper-soft);font-size:12px;line-height:1.65}.field-line,.boundary-line,.hierarchy-line{display:flex;align-items:center;gap:12px;flex-wrap:wrap;padding:16px 0;border-top:1px solid var(--line);border-bottom:1px solid var(--line)}.field-line span{color:var(--muted);font-size:9px}.field-line strong{margin-right:18px;font-size:10px}.field-action{display:inline-flex;min-height:46px;align-items:center;gap:20px;margin-top:20px;padding:0 17px;border:1px solid var(--paper);color:var(--paper)!important;text-decoration:none!important;font-size:11px;transition:background .16s ease,color .16s ease}.field-action:hover,.field-action:focus-visible{background:var(--paper);color:var(--space)!important;outline:3px solid rgba(244,240,228,.18);outline-offset:2px}
    .field-stream{border-top:1px solid var(--line)}.field-row{display:grid;grid-template-columns:180px 1fr 250px;gap:28px;align-items:start;padding:26px 0;border-bottom:1px solid var(--line-soft);scroll-margin-top:84px}.field-row:target{border-color:var(--seed)}.field-index span{display:block;color:var(--leaf);font-size:9px}.field-index small{display:block;margin-top:4px;color:var(--muted);font-size:8px}.field-copy h3{margin:0 0 7px;font-size:22px}.field-copy p{margin:0;color:var(--paper-soft);font-size:11px}.field-copy ul{display:flex;flex-wrap:wrap;gap:8px;margin:12px 0 0;padding:0;list-style:none}.field-copy li{padding-bottom:2px;border-bottom:1px solid var(--line);color:var(--muted);font-size:9px}.field-row details summary{min-height:40px;display:flex;align-items:center;color:var(--seed);font-size:9px;cursor:pointer}
    .six-w{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:1px;margin:10px 0 0;background:var(--line-soft)}.six-w div{padding:9px;background:#162b31}.six-w dt{color:var(--seed);font-size:8px}.six-w dt small{margin-left:4px;color:var(--muted)}.six-w dd{margin:4px 0 0;color:var(--paper-soft);font-size:9px;line-height:1.4}.boundary-line strong{color:var(--seed);font-size:10px}.boundary-line span{margin-right:22px;color:var(--paper-soft);font-size:10px}.plain-list{margin-top:20px;border-top:1px solid var(--line-soft)}.plain-list p{display:grid;grid-template-columns:140px 1fr;gap:20px;margin:0;padding:15px 0;border-bottom:1px solid var(--line-soft)}.plain-list b{font-size:11px}.plain-list span{color:var(--paper-soft);font-size:10px;line-height:1.55}.hierarchy-line{justify-content:center}.hierarchy-line span{font-size:10px}.hierarchy-line i{color:var(--seed);font-style:normal}.registry-lines{border-top:1px solid var(--line)}.registry-lines p{display:flex;justify-content:space-between;gap:20px;margin:0;padding:14px 0;border-bottom:1px solid var(--line-soft);font-size:10px}.registry-lines b{color:var(--leaf);text-align:right}.technical-disclosure{margin-top:18px}.technical-disclosure summary{min-height:44px;display:flex;align-items:center;color:var(--muted);cursor:pointer;font-size:9px}.technical-disclosure p{color:var(--paper-soft);font-size:10px}.core-context{padding-top:48px}.core-context h2{font-size:16px}.product-footer{display:flex!important;justify-content:space-between;max-width:1180px;margin:0 auto;padding:26px clamp(20px,4vw,54px);border-top:1px solid var(--line-soft);color:var(--muted);font-size:9px}
    [data-testid="stAppViewContainer"]:has(.integrated-platform) .block-container{max-width:1180px;padding:0 30px 72px!important}[data-testid="stAppViewContainer"]:has(.integrated-platform) h1,[data-testid="stAppViewContainer"]:has(.integrated-platform) h2,[data-testid="stAppViewContainer"]:has(.integrated-platform) h3{color:var(--paper);font-family:var(--font-ui)}.sapling-chamber{position:relative;min-height:360px;margin:32px 0 28px;padding:42px 36px 36px 170px;border-top:1px solid var(--line);border-bottom:1px solid var(--line);background:#162f35}.sapling-emblem{position:absolute;left:42px;top:46px;width:92px;height:108px;color:var(--leaf)}.sapling-chamber>span{color:var(--seed);font-size:9px;letter-spacing:.16em}.sapling-chamber h1{margin:8px 0;font-size:42px}.sapling-chamber p{max-width:720px;color:var(--paper-soft);font-size:12px;line-height:1.65}.sapling-chamber .seed-route{display:inline-flex;margin-top:12px;color:var(--muted);font-size:9px}.overview-chamber .sapling-emblem{color:var(--seed)}.overview-chamber .overview-return{display:flex;width:max-content}.subsystem-seeds{display:flex;gap:34px;margin-top:34px}.subsystem-seeds>span{display:grid;grid-template-columns:42px 1fr;grid-template-rows:auto auto;align-items:center;min-width:150px;min-height:74px;padding:4px 10px 0;border:1px solid var(--seed);border-bottom:5px solid #9f8755;border-radius:50% 50% 12% 12%/72% 72% 18% 18%;color:var(--paper)}.subsystem-seeds i{grid-row:1/3;width:32px;height:32px;color:var(--seed);font-style:normal}.subsystem-seeds b{font-size:11px}.subsystem-seeds small{color:var(--muted);font-size:8px}
    [data-testid="stAppViewContainer"]:has(.integrated-platform) [data-testid="stMetric"]{padding:14px 0;border-top:1px solid var(--line);border-bottom:1px solid var(--line);background:transparent}[data-testid="stAppViewContainer"]:has(.integrated-platform) [data-testid="stMetricLabel"] p{color:var(--paper-soft)}[data-testid="stAppViewContainer"]:has(.integrated-platform) [data-testid="stAlert"]{border:1px solid var(--line);border-radius:0!important;background:#162f35!important;color:var(--paper)!important}[data-testid="stAppViewContainer"]:has(.integrated-platform) [data-testid="stAlert"]>div{background:#162f35!important;color:var(--paper)!important}[data-testid="stAppViewContainer"]:has(.integrated-platform) [data-testid="stAlert"] p{color:var(--paper-soft)}[data-testid="stAppViewContainer"]:has(.integrated-platform) [data-testid="stDataFrame"]{border:1px solid var(--line)}[data-testid="stSpinner"]{color:var(--seed)}
    .sr-only{position:absolute!important;width:1px!important;height:1px!important;padding:0!important;margin:-1px!important;overflow:hidden!important;clip:rect(0,0,0,0)!important;white-space:nowrap!important;border:0!important}
    .official-world-shell .orientation-bar{position:absolute;inset:0 0 auto;z-index:30;min-height:0;padding:20px clamp(18px,3.2vw,52px);border:0;background:transparent;pointer-events:none}.official-world-shell .orientation-bar>*{pointer-events:auto}.official-world-shell .brand-home small,.official-world-shell .version-state{display:none}.official-world-shell .location-path{position:absolute;width:1px;height:1px;margin:-1px;overflow:hidden;clip:rect(0,0,0,0);white-space:nowrap}.official-world-shell .brand-home{padding:7px 10px 7px 7px;background:rgba(2,8,12,.58);border-bottom:1px solid rgba(215,187,120,.42)}.official-world-shell .brand-mark{width:30px;height:30px}.official-world-shell .home-return{position:relative;display:grid;width:46px;min-width:46px;height:46px;min-height:46px;padding:0;place-items:center;border-color:rgba(215,187,120,.55);border-radius:50%;background:rgba(2,8,12,.58)}.official-world-shell .home-return>b{position:absolute;top:51px;color:var(--paper);font-size:9px}.official-world-shell .home-return small{display:none}
    .official-world{position:relative;display:grid;min-height:100svh;overflow:hidden;place-items:center;background:#02070c}.world-stage{position:relative;width:min(100vw,177.68svh);height:auto;min-height:0;max-width:none;aspect-ratio:1672/941;margin:0 auto;overflow:hidden;background:#02070c}.official-world .ecosystem-key-visual{position:absolute;z-index:0;inset:0;width:100%;height:100%;object-fit:contain;object-position:center center}
    .core-signature{position:absolute;z-index:7;left:50%;top:26.5%;display:grid;min-height:44px;align-content:center;gap:3px;padding:5px 9px 4px;transform:translate(-50%,-50%);color:var(--paper)!important;text-align:center;text-decoration:none!important;text-shadow:0 2px 8px #000;cursor:pointer;transition:transform .18s cubic-bezier(.22,.61,.36,1),background .18s ease,box-shadow .18s ease}.core-signature strong{padding:4px 0 6px;border-bottom:1px solid rgba(215,187,120,.68);font-size:clamp(18px,1.8vw,31px);font-weight:550;letter-spacing:.035em}.core-action-hint{display:flex;align-items:center;justify-content:center;gap:6px;color:#ddd6c4;font-size:clamp(7px,.58vw,10px);letter-spacing:.04em}.core-action-hint b{color:var(--seed);font-size:11px}.core-action:hover,.core-action:focus-visible{transform:translate(-50%,calc(-50% - 2px));background:rgba(2,8,12,.28);box-shadow:0 8px 20px rgba(0,0,0,.18)!important}.core-action:focus-visible{outline:3px solid #f3f0e6!important;outline-offset:4px}.core-action:active{transform:translate(-50%,-50%) scale(.985);transition-duration:.08s}
    .project-seed-field{position:absolute;z-index:6;inset:0}.project-seed{--seed-accent:#d7bb78;position:absolute;display:flex;align-items:flex-end;justify-content:center;box-sizing:border-box;border:1px solid rgba(239,231,207,.08);border-radius:49% 49% 20% 20%/61% 61% 18% 18%;color:var(--paper)!important;text-decoration:none!important;isolation:isolate;cursor:pointer;will-change:transform;transition:transform .18s cubic-bezier(.22,.61,.36,1),border-color .18s ease,box-shadow .18s ease}.project-seed:after{content:"";position:absolute;z-index:-1;inset:1px;border:1px solid rgba(239,231,207,.18);border-radius:inherit;background:rgba(4,12,17,.012);transition:border-color .18s ease,background .18s ease}.project-seed:focus-visible{outline:3px solid #f3f0e6!important;outline-offset:4px;transform:translateY(-2px);border-color:rgba(248,243,228,.72);box-shadow:0 10px 22px rgba(0,0,0,.2)!important}.project-seed:focus-visible:after{border-color:rgba(248,243,228,.88);background:rgba(255,255,255,.024)}.project-seed:active{transform:translateY(0) scale(.985);transition-duration:.08s}.project-seed:active:after{background:rgba(255,255,255,.04)}.project-seed .mobile-seed-art{display:none}
    @media(hover:hover) and (pointer:fine){.project-seed:hover{transform:translateY(-3px) scale(1.01);border-color:rgba(248,243,228,.6);box-shadow:0 10px 22px rgba(0,0,0,.2)}.project-seed:hover:after{border-color:rgba(248,243,228,.88);background:rgba(255,255,255,.024)}.project-seed:hover .project-seed-label{background:rgba(2,8,12,.48)}.project-seed:hover .project-seed-label b{border-color:#fff;background:rgba(255,255,255,.08);transform:translateX(1px)}}.project-seed:focus-visible .project-seed-label{background:rgba(2,8,12,.48)}.project-seed:focus-visible .project-seed-label b{border-color:#fff;background:rgba(255,255,255,.08);transform:translateX(1px)}
    .project-seed-label{position:absolute;left:50%;bottom:8%;display:grid;grid-template-columns:minmax(0,1fr) 24px;column-gap:10px;min-width:150px;min-height:44px;box-sizing:border-box;padding:7px 8px 8px;transform:translateX(-50%);border-bottom:1px solid var(--seed-accent);border-radius:6px 6px 0 0;background:rgba(2,8,12,.34);text-align:left;text-shadow:0 2px 6px #000;box-shadow:0 3px 10px rgba(0,0,0,.16);transition:background .18s ease}.project-seed-label strong,.project-seed-label em,.project-seed-label b{display:block}.project-seed-label strong{grid-column:1;margin:0;color:#fff;font-size:clamp(13px,1.1vw,18px);font-weight:600;line-height:1.15;letter-spacing:.005em;white-space:nowrap}.project-seed-label em{grid-column:1;margin-top:3px;color:#e0e5df;font-size:clamp(7px,.58vw,10px);font-style:normal;line-height:1.35}.project-seed-label b{grid-column:2;grid-row:1/3;display:grid;width:22px;height:22px;align-self:center;place-items:center;border:1px solid var(--seed-accent);border-radius:50%;color:#fff;font-size:11px;font-weight:600;transition:transform .16s ease,border-color .16s ease,background .16s ease}.project-seed:active .project-seed-label b{transform:scale(.9)}.project-seed.node-living{left:16.7%;top:26%;width:17%;height:61%;--seed-accent:#b8d27e}.project-seed.node-learning{left:68.1%;top:26%;width:17%;height:61%;--seed-accent:#91c4e5}.project-seed.node-ai{left:44.1%;top:58%;width:14.3%;height:41%;--seed-accent:#d8b66d}.project-seed.node-learning .project-seed-label{min-width:215px}.project-seed.node-ai .project-seed-label{bottom:6%}.is-unavailable.project-seed{opacity:.55;cursor:not-allowed;pointer-events:none}
    @media(max-width:1100px) and (min-width:701px){.project-node{width:240px}.project-node.node-living{left:2%}.project-node.node-learning{right:2%}.project-node.node-ai{right:3%}.seed-garden{left:10%;right:10%}.root-foundation{left:2%;right:2%}.field-row{grid-template-columns:130px 1fr}.field-row details{grid-column:2}.context-columns{grid-template-columns:1fr}.context-columns>section{border-right:0;border-bottom:1px solid var(--line-soft)}.official-world .project-seed-label{min-width:140px}.official-world .project-seed.node-learning .project-seed-label{min-width:190px}}
    @media(max-width:1100px) and (min-width:701px) and (orientation:portrait){.official-world{grid-template-rows:0 auto;align-content:start;place-items:start center;padding-top:74px}.official-world .world-stage{align-self:start}}
    @media(max-width:700px){.orientation-bar{position:relative;grid-template-columns:1fr auto;gap:10px;min-height:74px;padding:10px 14px}.brand-lockup{display:block}.brand-mark{width:30px;height:30px}.brand-home small,.version-state{display:none}.location-path{grid-column:1/3;padding:0}.location-path span{font-size:8px}.location-path strong{font-size:9px}.home-return{grid-column:2;grid-row:1;min-width:54px;justify-content:center}.home-return small{display:none}.atlas-stage{min-height:auto;overflow:visible}.atlas-stage:after{display:none}.atlas-heading{position:relative;left:auto;top:auto;padding:18px 18px 8px;text-shadow:none}.atlas-heading h1{font-size:26px}.atlas-heading p{color:var(--paper-soft);font-size:10px}.atlas-status{position:relative;right:auto;top:auto;margin:0 18px 10px;text-shadow:none}.cosmic-lineage{position:relative;left:auto;right:auto;top:auto;width:auto;margin:0 14px 12px;transform:none;grid-template-columns:repeat(4,1fr);border-top:1px solid var(--line-soft);border-bottom:1px solid var(--line-soft);padding:8px 0}.cosmic-lineage li{padding:0 3px}.cosmic-lineage li:not(:last-child):after{right:-3px;top:9px}.cosmic-lineage small{font-size:6px}.cosmic-lineage b{font-size:7px}.world-atlas{height:auto;min-height:0;margin:0 14px;padding:0 0 26px;display:flex;flex-direction:column;gap:6px;background:var(--space)}.world-atlas:after{content:"";position:absolute;z-index:0;left:28px;top:184px;bottom:30px;width:1px;background:var(--line-soft)}.ecosystem-key-visual{position:relative;inset:auto;order:1;box-sizing:border-box;width:100%;height:188px;margin:8px 0 4px;border:1px solid rgba(216,189,125,.38);border-radius:46% 46% 12% 12%/24% 24% 8% 8%;object-fit:cover;object-position:center 43%}.fruit-universe{display:none}.ecosystem-tree{display:none}.mobile-layer{position:relative;z-index:3;display:flex;align-items:baseline;gap:8px;margin:10px 0 2px;padding-left:48px;color:var(--seed)}.mobile-layer:before{content:"";position:absolute;left:22px;top:5px;width:12px;height:12px;border:2px solid var(--seed);border-radius:50%;background:var(--space)}.mobile-layer span{font-size:8px;letter-spacing:.12em}.mobile-layer b{color:var(--paper);font-size:13px}.layer-core{display:none}.core-landmark{order:2}.layer-projects{order:3}.node-living{order:4}.node-learning{order:5}.node-ai{order:6}.layer-seeds{order:7}.seed-garden{order:8}.layer-roots{order:9}.root-foundation{order:10}.core-landmark{position:relative;left:auto;top:auto;z-index:3;align-self:center;box-sizing:border-box;width:min(76%,270px);min-height:98px;margin-top:-104px;padding:7px 12px 9px;transform:none;background:rgba(7,18,22,.82);border:1px solid rgba(158,189,121,.62);text-shadow:0 2px 6px #000}.core-landmark .node-icon{width:54px;height:54px}.core-landmark .node-copy strong{font-size:17px}.core-landmark .node-copy span{font-size:8px}.core-landmark.is-selected:after{margin-top:4px}.project-node{position:relative;inset:auto;z-index:3;box-sizing:border-box;grid-template-columns:92px 1fr;width:100%;min-height:128px;padding:8px 10px 8px 38px;background:var(--space);text-shadow:none;transform:none}.project-node:hover{transform:translateY(-2px)}.sapling-figure{width:78px;height:94px}.seed-garden{position:relative;inset:auto;z-index:3;display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:12px;padding:4px 0;background:var(--space)}.seed-node{width:100%;min-height:126px;padding:8px 4px;text-shadow:none}.seed-guide{grid-column:1/-1;width:50%;justify-self:center}.seed-dome{width:72px;height:62px}.seed-node .node-copy>span{display:none}.root-foundation{position:relative;inset:auto;z-index:3;display:grid;gap:8px;background:var(--space)}.root-node{box-sizing:border-box;width:100%;min-height:68px;padding:8px 10px 8px 38px;background:var(--space);text-shadow:none}.context-drawer{margin:0 14px}.field-zone,.core-context{padding:58px 18px}.field-zone>header{grid-template-columns:1fr;gap:8px}.field-zone>header>span,.field-zone>header h2,.field-zone>header p{grid-column:1;grid-row:auto}.field-zone>header h2{font-size:28px}.field-line,.boundary-line{align-items:flex-start;flex-direction:column}.field-row{grid-template-columns:1fr;gap:14px;padding:22px 0}.field-row details{grid-column:1}.plain-list p{grid-template-columns:1fr;gap:6px}.hierarchy-line{justify-content:flex-start}.registry-lines p{align-items:flex-start}.six-w{grid-template-columns:1fr}.product-footer{display:block!important}.product-footer span{display:block;margin-bottom:5px}[data-testid="stAppViewContainer"]:has(.integrated-platform) .block-container{padding:0 14px 50px!important}.sapling-chamber{min-height:0;margin:20px 0;padding:132px 20px 24px}.sapling-emblem{left:20px;top:18px;width:80px;height:96px}.sapling-chamber h1{font-size:34px}.subsystem-seeds{display:grid;grid-template-columns:1fr;gap:14px}.subsystem-seeds>span{box-sizing:border-box;width:100%;min-height:78px}}
    @media(max-width:700px){.official-world-shell .orientation-bar{position:absolute;grid-template-columns:1fr auto;padding:10px 12px}.official-world-shell .brand-home{padding:5px 8px 5px 5px}.official-world-shell .brand-home strong{font-size:12px}.official-world-shell .brand-mark{width:27px;height:27px}.official-world-shell .home-return{grid-column:2;grid-row:1;width:42px;min-width:42px;height:42px;min-height:42px}.official-world-shell .home-return>b{top:45px;font-size:8px}.official-world{display:block;min-height:100svh;padding-top:64px;overflow:visible}.official-world .world-stage{display:flex;width:100%;height:auto;min-height:0;margin:0;aspect-ratio:auto;overflow:visible;flex-direction:column;background:#02070c}.official-world .ecosystem-key-visual{position:relative;inset:auto;order:1;width:100%;height:auto;aspect-ratio:1672/941;object-fit:cover;object-position:center center}.official-world .core-signature{left:50%;top:11.8vw;min-height:44px;padding:4px 7px}.official-world .core-signature strong{padding-bottom:4px;font-size:clamp(12px,3.8vw,16px)}.official-world .core-action-hint{gap:4px;font-size:7px}.project-seed-field{position:relative;inset:auto;order:2;display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:10px 4px;align-items:start;padding:12px 8px 30px;background:#02070c}.project-seed,.project-seed.node-living,.project-seed.node-learning,.project-seed.node-ai{position:relative;left:auto;right:auto;top:auto;bottom:auto;display:flex;width:100%;height:auto;min-height:274px;border-color:rgba(239,231,207,.2);border-radius:49% 49% 20% 20%/61% 61% 18% 18%;overflow:hidden;transform:none;will-change:auto}.project-seed.node-living,.project-seed.node-learning{aspect-ratio:455/690}.project-seed.node-ai{grid-column:1/-1;justify-self:center;width:62%;min-height:240px;aspect-ratio:470/441}.project-seed:focus-visible{transform:none;outline-offset:3px}.project-seed:active{transform:scale(.99)}.project-seed .mobile-seed-art{position:absolute;display:block;inset:0;width:100%;height:100%;object-fit:cover}.project-seed.node-living .mobile-seed-art,.project-seed.node-learning .mobile-seed-art,.project-seed.node-ai .mobile-seed-art{object-position:center center}.project-seed-label,.project-seed.node-learning .project-seed-label{left:50%;bottom:7%;box-sizing:border-box;width:84%;min-width:0;padding:7px 8px 8px}.project-seed.node-ai .project-seed-label{bottom:5%}.project-seed-label strong{font-size:clamp(13px,3.6vw,16px);white-space:normal}.project-seed-label em{font-size:9px}.project-seed-label b{width:22px;height:22px;font-size:10px}}
    @media(prefers-reduced-motion:reduce){*{transition:none!important;scroll-behavior:auto!important}}
    </style>''')


def render_ai_hub() -> None:
    """Render AI Hub inside the shared OS Ecosystem product shell."""
    source = str(AI_HUB_SOURCE)
    if source not in sys.path:
        sys.path.insert(0, source)
    from ai_hub.presentation.operator_ui.app import build_initial_snapshot
    from ai_hub.presentation.operator_ui.pages.dashboard import render_dashboard

    st.markdown(f'''
    <main class="integrated-platform">
      {_orientation_markup("AI Hub")}
      <section class="sapling-chamber" aria-labelledby="ai-title">
        <span class="sapling-emblem" aria-hidden="true">{_icon_svg("sapling")}</span>
        <span>묘목 · 내부 프로젝트</span>
        <h1 id="ai-title">AI Hub</h1>
        <p>OS Ecosystem 안에서 승인된 AI 연결 상태, 선택 경로와 안전한 실행 기록을 확인합니다. 인증 정보와 원문 데이터는 표시하지 않습니다.</p>
        <span class="seed-route">OS Ecosystem / AI Hub</span>
        <div class="subsystem-seeds" aria-label="AI Hub 내부 돔형 씨앗">
          <span><i aria-hidden="true">{_icon_svg("connection")}</i><b>AI 연결</b><small>Subsystem</small></span>
          <span><i aria-hidden="true">{_icon_svg("guide")}</i><b>경로 선택</b><small>Engine</small></span>
          <span><i aria-hidden="true">{_icon_svg("record")}</i><b>실행 기록</b><small>Module</small></span>
        </div>
      </section>
    </main>''', unsafe_allow_html=True)
    render_dashboard(build_initial_snapshot(), st)


def render_ecosystem_overview() -> None:
    """Render the repository-owned OS Ecosystem overview route."""
    st.markdown(f'''
    <main class="integrated-platform">
      {_orientation_markup("Overview")}
      <section class="sapling-chamber overview-chamber" aria-labelledby="overview-title">
        <span class="sapling-emblem" aria-hidden="true">{_icon_svg("core")}</span>
        <span>현재 세계 · 통합 상태</span>
        <h1 id="overview-title">OS Ecosystem Overview</h1>
        <p>OS Ecosystem의 프로젝트 연결과 현재 운영 상태를 확인하는 내부 화면입니다. 세부 운영 정보는 승인된 프로젝트 화면에서 관리합니다.</p>
        <span class="seed-route">OS Ecosystem / Overview</span>
        <a class="field-action overview-return" href="./" target="_self" rel="noopener noreferrer">세계로 돌아가기 <span aria-hidden="true">←</span></a>
      </section>
    </main>''', unsafe_allow_html=True)


def main() -> None:
    st.set_page_config(
        page_title="OS Ecosystem",
        page_icon="🌳",
        layout="wide",
        initial_sidebar_state="collapsed",
    )
    apply_theme()
    if st.query_params.get("project") == "ai-hub":
        render_ai_hub()
        return
    if st.query_params.get("view") == "overview":
        render_ecosystem_overview()
        return
    render_launcher(get_projects())


if __name__ == "__main__":
    main()
