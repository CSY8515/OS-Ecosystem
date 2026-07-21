"""OS Ecosystem v0.2.3 — unified launcher for independent projects."""

from __future__ import annotations

import html
import os
from dataclasses import dataclass
from urllib.parse import urlparse

import streamlit as st


VERSION = "0.2.3"


@dataclass(frozen=True)
class Project:
    """Public launcher metadata. Internal implementation details stay private."""

    name: str
    label: str
    description: str
    url: str | None
    position: str


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
    """Return the initial public project catalog."""
    return (
        Project(
            name="Living OS",
            label="LIVING",
            description="삶의 기록과 운영을 하나의 흐름으로",
            url=_configured_url(
                "LIVING_OS_URL",
                "https://living-os-h5uinmvmjpvv6m8phat28a.streamlit.app/",
            ),
            position="node-left",
        ),
        Project(
            name="Universal Learning Engine",
            label="LEARNING",
            description="어떤 주제든 구조화된 학습 경험으로",
            url=_configured_url(
                "ULE_URL",
                "https://universal-learning-engine-zb5aezuadeu84gnqust8mw.streamlit.app/",
            ),
            position="node-right",
        ),
    )


def _project_node(project: Project) -> str:
    name = html.escape(project.name)
    label = html.escape(project.label)
    description = html.escape(project.description)
    classes = f"project-node {project.position}"
    if project.url:
        url = html.escape(project.url, quote=True)
        return f"""
        <a class="{classes}" href="{url}" target="_blank" rel="noopener noreferrer" aria-label="{name} 열기">
          <span class="node-orbit" aria-hidden="true"></span>
          <span class="node-index">CONNECTED PROJECT</span>
          <strong>{name}</strong>
          <span class="node-copy">{description}</span>
          <span class="node-action">{label} OS 열기 <span aria-hidden="true">↗</span></span>
        </a>
        """
    return f"""
    <div class="{classes} is-pending" aria-label="{name} 연결 준비 중">
      <span class="node-orbit" aria-hidden="true"></span>
      <span class="node-index">CONNECTION PENDING</span>
      <strong>{name}</strong>
      <span class="node-copy">{description}</span>
      <span class="node-action">배포 주소 연결 필요</span>
    </div>
    """


def render_launcher(projects: tuple[Project, ...]) -> None:
    nodes = "".join(_project_node(project) for project in projects)
    st.html(
        f"""
        <main class="ecosystem-shell">
          <div id="projects" class="anchor-target"></div>
          <nav class="ecosystem-nav" aria-label="Ecosystem menu">
            <a href="#projects">Projects</a>
            <a href="#governance">Governance</a>
            <a href="#architecture">Architecture</a>
            <a href="#registry">Registry</a>
          </nav>
          <div class="ambient ambient-one"></div>
          <div class="ambient ambient-two"></div>
          <section class="ecosystem-stage" aria-label="OS Ecosystem 프로젝트 런처">
            <div class="connection-line line-left" aria-hidden="true"></div>
            <div class="connection-line line-right" aria-hidden="true"></div>
            {nodes}
            <div class="ecosystem-core">
              <span class="core-eyebrow">INTEGRATED LAUNCHER</span>
              <div class="core-mark" aria-hidden="true"><i></i><i></i><i></i></div>
              <h1>OS<br><span>ECOSYSTEM</span></h1>
              <p>독립된 시스템을 연결하는 하나의 시작점</p>
              <span class="core-status"><i></i> SYSTEM ONLINE · v{VERSION}</span>
            </div>
          </section>

          <div class="ecosystem-layers">
            <section class="ecosystem-section" id="governance">
              <header class="section-heading">
                <span class="section-kicker">01 / GOVERNANCE</span>
                <h2>Governance</h2>
                <p>The shared authority layer for independent systems.</p>
              </header>
              <div class="ecosystem-grid governance-grid">
                <article class="ecosystem-item">
                  <span class="item-index">GOV-01</span>
                  <h3>Ecosystem Constitution</h3>
                  <p>Defines authority, project autonomy, ownership, and the boundaries of the ecosystem layer.</p>
                </article>
                <article class="ecosystem-item">
                  <span class="item-index">GOV-02</span>
                  <h3>Ecosystem Rules</h3>
                  <p>Controls project connection, approved changes, releases, and operational accountability.</p>
                </article>
                <article class="ecosystem-item">
                  <span class="item-index">GOV-03</span>
                  <h3>Ecosystem Principles</h3>
                  <p>Preserves autonomy, explicit consent, traceability, reversibility, and clear ownership.</p>
                </article>
                <article class="ecosystem-item">
                  <span class="item-index">GOV-04</span>
                  <h3>Ecosystem Standards</h3>
                  <p>Sets common expectations for compatibility, documentation, testing, and releases.</p>
                </article>
                <article class="ecosystem-item">
                  <span class="item-index">GOV-05</span>
                  <h3>Ecosystem Policies</h3>
                  <p>Records approval, maintenance, deprecation, security, and publication policy.</p>
                </article>
              </div>
            </section>

            <section class="ecosystem-section" id="architecture">
              <header class="section-heading">
                <span class="section-kicker">02 / ARCHITECTURE</span>
                <h2>Architecture</h2>
                <p>The structural map for projects that remain independent by design.</p>
              </header>
              <div class="ecosystem-grid architecture-grid">
                <article class="ecosystem-item">
                  <span class="item-index">ARC-01</span>
                  <h3>Master Architecture</h3>
                  <p>OS Ecosystem is the governance, registry, and navigation layer above autonomous project runtimes.</p>
                </article>
                <article class="ecosystem-item">
                  <span class="item-index">ARC-02</span>
                  <h3>Repository Strategy</h3>
                  <p>Each project keeps an independent repository, version history, test suite, and release lifecycle.</p>
                </article>
                <article class="ecosystem-item">
                  <span class="item-index">ARC-03</span>
                  <h3>Integration Strategy</h3>
                  <p>Connections use explicit public contracts and direct application links without runtime merging.</p>
                </article>
                <article class="ecosystem-item">
                  <span class="item-index">ARC-04</span>
                  <h3>Roadmap</h3>
                  <p>Expand governance and registry depth before onboarding additional independent projects.</p>
                </article>
              </div>
            </section>

            <section class="ecosystem-section" id="registry">
              <header class="section-heading">
                <span class="section-kicker">03 / REGISTRY</span>
                <h2>Registry</h2>
                <p>The authoritative index of ecosystem membership and releases.</p>
              </header>
              <div class="ecosystem-grid registry-grid">
                <article class="ecosystem-item registry-item">
                  <span class="item-index">REG-01</span>
                  <h3>Project Registry</h3>
                  <div class="registry-row"><span>Living OS</span><b>v2.0.4 · STABLE</b></div>
                  <div class="registry-row"><span>Universal Learning Engine</span><b>v1.0.0 · STABLE</b></div>
                </article>
                <article class="ecosystem-item registry-item">
                  <span class="item-index">REG-02</span>
                  <h3>Capability Registry</h3>
                  <div class="registry-row"><span>Safety Capability</span><b>v1.0.0 · INTERNAL</b></div>
                  <p>Capability details remain governed and hidden from project navigation.</p>
                </article>
                <article class="ecosystem-item registry-item">
                  <span class="item-index">REG-03</span>
                  <h3>Release History</h3>
                  <div class="registry-row"><span>v0.2.3</span><b>ECOSYSTEM LAYER</b></div>
                  <div class="registry-row"><span>v0.2.2</span><b>UI STABILITY</b></div>
                  <div class="registry-row"><span>v0.2.1</span><b>PROJECT CONNECTIONS</b></div>
                </article>
              </div>
            </section>
          </div>
          <footer>
            <span>SELECT A PROJECT TO ENTER</span>
            <span>SEOUL · KST</span>
          </footer>
        </main>
        """,
    )


def apply_theme() -> None:
    st.html(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Manrope:wght@500;600;700&display=swap');

        :root { --ink:#eef4f4; --muted:#7f9294; --line:rgba(143,225,219,.19); --cyan:#8fe1db; --bg:#071011; }
        html, body, [data-testid="stAppViewContainer"] { background:var(--bg); }
        [data-testid="stHeader"], [data-testid="stSidebar"], [data-testid="stToolbar"], footer { display:none !important; }
        .stApp { color:var(--ink); background:
          radial-gradient(circle at 50% 45%, rgba(38,111,107,.11), transparent 28rem),
          linear-gradient(rgba(143,225,219,.024) 1px, transparent 1px),
          linear-gradient(90deg, rgba(143,225,219,.024) 1px, transparent 1px), #071011;
          background-size:auto, 52px 52px, 52px 52px, auto;
        }
        .block-container { max-width:none; padding:0 !important; }
        .ecosystem-shell { min-height:100vh; position:relative; overflow:hidden; font-family:Inter,sans-serif; }
        .anchor-target { position:absolute; top:0; }
        .ecosystem-nav { position:absolute; z-index:10; top:24px; left:50%; transform:translateX(-50%); display:flex; align-items:center; padding:5px; border:1px solid rgba(143,225,219,.12); background:rgba(7,16,17,.78); backdrop-filter:blur(18px); }
        .ecosystem-nav a { padding:10px 15px; color:#819395 !important; text-decoration:none !important; font-size:9px; letter-spacing:.16em; text-transform:uppercase; transition:color .2s ease,background .2s ease; }
        .ecosystem-nav a:hover,.ecosystem-nav a:focus-visible { color:var(--cyan) !important; background:rgba(143,225,219,.07); outline:none; }
        .ecosystem-layers { position:relative; border-top:1px solid rgba(143,225,219,.08); background:linear-gradient(180deg,rgba(7,16,17,.92),rgba(5,12,13,.98)); }
        .ecosystem-section { max-width:1120px; margin:0 auto; padding:104px 34px; scroll-margin-top:24px; }
        .ecosystem-section + .ecosystem-section { border-top:1px solid rgba(143,225,219,.08); }
        .section-heading { display:grid; grid-template-columns:180px 1fr; column-gap:30px; align-items:end; margin-bottom:38px; }
        .section-kicker,.item-index { color:#607476; font-size:9px; letter-spacing:.2em; }
        .section-heading h2 { margin:0; font:500 38px/1 Manrope,sans-serif; letter-spacing:-.04em; }
        .section-heading p { grid-column:2; margin:12px 0 0; color:#7f9294; font-size:12px; }
        .ecosystem-grid { display:grid; gap:1px; padding:1px; background:rgba(143,225,219,.09); }
        .governance-grid { grid-template-columns:repeat(5,1fr); }
        .architecture-grid { grid-template-columns:repeat(4,1fr); }
        .registry-grid { grid-template-columns:repeat(3,1fr); }
        .ecosystem-item { min-height:210px; padding:27px; background:#091415; }
        .ecosystem-item h3 { margin:34px 0 13px; font:600 16px/1.25 Manrope,sans-serif; letter-spacing:-.025em; }
        .ecosystem-item p { margin:0; color:#758789; font-size:11px; line-height:1.7; }
        .registry-item { min-height:230px; }
        .registry-row { display:flex; justify-content:space-between; gap:18px; padding:13px 0; border-bottom:1px solid rgba(143,225,219,.08); color:#b7c5c5; font-size:10px; }
        .registry-row:first-of-type { margin-top:24px; }
        .registry-row b { color:var(--cyan); font-size:8px; letter-spacing:.08em; font-weight:500; text-align:right; }
        .registry-item p { margin-top:18px; }
        .ecosystem-stage { min-height:calc(100vh - 78px); position:relative; display:grid; place-items:center; }
        .ecosystem-core { width:330px; height:330px; border:1px solid rgba(143,225,219,.24); border-radius:50%; display:flex; flex-direction:column; align-items:center; justify-content:center; text-align:center; position:relative; z-index:3; background:radial-gradient(circle at 50% 40%, rgba(22,55,55,.96), rgba(7,16,17,.97) 67%); box-shadow:0 0 0 22px rgba(143,225,219,.025), 0 0 0 23px rgba(143,225,219,.07), 0 34px 90px rgba(0,0,0,.45); }
        .ecosystem-core:before,.ecosystem-core:after { content:""; position:absolute; border-radius:50%; border:1px dashed rgba(143,225,219,.11); inset:-55px; animation:spin 45s linear infinite; }
        .ecosystem-core:after { inset:-95px; animation-direction:reverse; animation-duration:70s; }
        .core-eyebrow,.node-index,.ecosystem-shell footer { font-size:10px; letter-spacing:.24em; color:var(--muted); }
        .core-mark { display:flex; gap:5px; margin:18px 0 14px; }
        .core-mark i { width:6px; height:6px; border-radius:50%; border:1px solid var(--cyan); }
        .core-mark i:nth-child(2) { background:var(--cyan); box-shadow:0 0 18px var(--cyan); }
        .ecosystem-core h1 { font-family:Manrope,sans-serif; margin:0; font-size:34px; line-height:.92; letter-spacing:-.05em; font-weight:500; }
        .ecosystem-core h1 span { font-size:37px; color:var(--cyan); }
        .ecosystem-core p { max-width:230px; color:#91a2a3; font-size:12px; margin:18px 0 20px; }
        .core-status { font-size:9px; letter-spacing:.14em; color:#718384; }
        .core-status i { display:inline-block; width:5px; height:5px; margin-right:7px; border-radius:50%; background:#75e3ae; box-shadow:0 0 10px #75e3ae; }
        .project-node { width:250px; min-height:188px; box-sizing:border-box; position:absolute; z-index:4; top:50%; transform:translateY(-50%); padding:26px; color:var(--ink) !important; text-decoration:none !important; border:1px solid rgba(143,225,219,.16); background:linear-gradient(145deg,rgba(13,29,30,.94),rgba(8,18,19,.94)); transition:transform .25s ease,border-color .25s ease,background .25s ease; }
        .project-node:hover { transform:translateY(-50%) scale(1.025); border-color:rgba(143,225,219,.6); background:linear-gradient(145deg,rgba(18,42,42,.98),rgba(8,18,19,.98)); }
        .node-left { right:calc(50% + 310px); }
        .node-right { left:calc(50% + 310px); }
        .project-node strong { font:600 20px/1.15 Manrope,sans-serif; display:block; margin:18px 0 10px; letter-spacing:-.03em; }
        .node-copy { display:block; min-height:38px; font-size:11px; line-height:1.65; color:#859697; }
        .node-action { display:block; margin-top:20px; padding-top:15px; border-top:1px solid rgba(143,225,219,.1); color:var(--cyan); font-size:10px; letter-spacing:.08em; }
        .node-orbit { position:absolute; top:17px; right:18px; width:8px; height:8px; border:1px solid var(--cyan); border-radius:50%; box-shadow:0 0 14px rgba(143,225,219,.7); }
        .is-pending { opacity:.54; cursor:not-allowed; }
        .is-pending .node-orbit { border-color:#6c797a; box-shadow:none; }
        .is-pending .node-action { color:#7f9294; }
        .connection-line { position:absolute; z-index:2; top:50%; height:1px; width:215px; background:linear-gradient(90deg,transparent,var(--line)); }
        .line-left { right:calc(50% + 165px); }
        .line-right { left:calc(50% + 165px); transform:rotate(180deg); }
        .ambient { position:absolute; width:380px; height:380px; border-radius:50%; filter:blur(120px); opacity:.08; background:#8fe1db; }
        .ambient-one { left:-180px; top:-180px; }.ambient-two { right:-200px; bottom:-200px; }
        .ecosystem-shell footer { height:78px; padding:0 36px; display:flex !important; align-items:center; justify-content:space-between; border-top:1px solid rgba(143,225,219,.08); }
        @keyframes spin { to { transform:rotate(360deg); } }
        @media (max-width:1050px) {
          .ecosystem-stage { min-height:auto; padding:110px 24px 50px; display:flex; flex-direction:column; gap:34px; }
          .ecosystem-core { order:1; width:280px; height:280px; }
          .project-node { order:2; position:relative; top:auto; left:auto; right:auto; transform:none; width:min(100%,420px); min-height:160px; }
          .project-node:hover { transform:scale(1.015); }
          .connection-line { display:none; }
          .node-right { order:3; }
          .ecosystem-nav { width:calc(100% - 32px); justify-content:center; flex-wrap:wrap; }
          .ecosystem-nav a { padding:9px 10px; font-size:8px; }
          .ecosystem-section { padding:74px 24px; }
          .section-heading { grid-template-columns:1fr; }
          .section-heading h2 { margin-top:18px; }
          .section-heading p { grid-column:1; }
          .governance-grid,.architecture-grid,.registry-grid { grid-template-columns:1fr; }
          .ecosystem-item { min-height:auto; }
        }
        @media (prefers-reduced-motion:reduce) { * { animation:none !important; transition:none !important; } }
        </style>
        """,
    )


def main() -> None:
    st.set_page_config(
        page_title="OS Ecosystem",
        page_icon="◉",
        layout="wide",
        initial_sidebar_state="collapsed",
    )
    apply_theme()
    render_launcher(get_projects())


if __name__ == "__main__":
    main()
