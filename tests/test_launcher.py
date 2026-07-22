import os
import unittest
from pathlib import Path
from unittest.mock import patch

import app
from streamlit.testing.v1 import AppTest


class LauncherContractTests(unittest.TestCase):
    def test_version_matches_release(self):
        self.assertEqual(app.VERSION, "0.7.0")

    def test_initial_catalog_contains_official_systems(self):
        self.assertEqual(
            [project.name for project in app.get_projects()],
            ["Living OS", "Universal Learning Engine", "AI Hub"],
        )

    def test_ai_hub_uses_repository_internal_dashboard(self):
        project = next(item for item in app.get_projects() if item.name == "AI Hub")
        self.assertEqual(project.url, "?project=ai-hub")
        rendered = app._project_node(project)
        self.assertIn('href="?project=ai-hub"', rendered)
        self.assertNotIn('target="_blank"', rendered)

    def test_valid_environment_destination_is_accepted(self):
        with patch.dict(os.environ, {"ULE_URL": "https://ule.example.com"}, clear=False):
            self.assertEqual(app._configured_url("ULE_URL"), "https://ule.example.com")

    def test_unsafe_destination_is_rejected(self):
        with patch.dict(os.environ, {"ULE_URL": "javascript:alert(1)"}, clear=False):
            self.assertIsNone(app._configured_url("ULE_URL"))

    def test_missing_destination_renders_unavailable_state(self):
        rendered = app._project_node(app.Project("Example", "EXAMPLE", "Description", None, "node-left"))
        self.assertIn("연결 준비 중", rendered)
        self.assertIn("승인된 배포 주소가 필요합니다", rendered)
        self.assertNotIn("href=", rendered)

    def test_connected_destination_is_html_escaped(self):
        project = app.Project("Example", "EXAMPLE", "Description", "https://example.com/?a=1&b=2", "node-left")
        self.assertIn("a=1&amp;b=2", app._project_node(project))

    def test_connected_destination_opens_directly_in_new_tab(self):
        rendered = app._project_node(
            app.Project("Example", "EXAMPLE", "Description", "https://example.com/app", "node-left")
        )
        self.assertIn('href="https://example.com/app"', rendered)
        self.assertIn('target="_blank"', rendered)
        self.assertIn('rel="noopener noreferrer"', rendered)
        self.assertNotIn("share.streamlit.io", rendered)

    def test_external_production_urls_are_direct_streamlit_apps(self):
        external = [item for item in app.get_projects() if item.name != "AI Hub"]
        for project in external:
            self.assertTrue(project.url.startswith("https://"))
            self.assertTrue(project.url.endswith(".streamlit.app/"))
            self.assertNotIn("share.streamlit.io", project.url)

    def test_korean_first_product_header_navigation_and_breadcrumb(self):
        markup = app._product_header_markup("Home")
        for korean, english in (
            ("홈", "Home"), ("프로젝트", "Projects"), ("AI 허브", "AI Hub"),
            ("역량", "Capabilities"), ("거버넌스", "Governance"),
            ("아키텍처", "Architecture"), ("레지스트리", "Registry"),
        ):
            self.assertIn(f"<span>{korean}</span><small>{english}</small>", markup)
        self.assertIn('class="breadcrumb"', markup)
        self.assertIn("<strong>홈</strong>", markup)

    def test_ecosystem_sections_and_architecture_are_rendered(self):
        with patch.object(app.st, "html") as html_renderer:
            app.render_launcher(app.get_projects())
        markup = html_renderer.call_args.args[0]
        for section_id in ("projects", "ai-hub", "capability", "automation", "connectivity", "secretary", "governance", "architecture", "registry"):
            self.assertIn(f'id="{section_id}"', markup)
        for item in (
            "Ecosystem Constitution", "Ecosystem Rules", "Ecosystem Principles",
            "Ecosystem Standards", "Ecosystem Policies", "Master Architecture",
            "Repository Strategy", "Integration Strategy", "Roadmap",
            "Capability Architecture", "Project Registry", "Capability Registry",
            "Release History", "6W Metadata",
        ):
            self.assertIn(item, markup)

    def test_ai_hub_entry_and_project_registry_are_rendered(self):
        with patch.object(app.st, "html") as html_renderer:
            app.render_launcher(app.get_projects())
        markup = html_renderer.call_args.args[0]
        self.assertIn('id="ai-hub"', markup)
        self.assertIn("AI Hub 운영 요약", markup)
        self.assertIn("OpenAI / Gemini / Claude", markup)
        self.assertIn('href="?project=ai-hub"', markup)
        self.assertIn("AI Hub 운영 화면 열기", markup)
        self.assertIn("AI Hub</span><b>v0.1.0 · 통합", markup)

    def test_every_system_and_capability_has_complete_six_w_metadata(self):
        values = [app.get_project_metadata(item) for item in app.get_projects()]
        values.extend(item.metadata for item in app.get_capabilities())
        for metadata in values:
            self.assertTrue(all(getattr(metadata, name).strip() for name in ("who", "when", "where", "what", "how", "why")))
        markup = app._six_w_markup(values[0])
        for english, korean in (("Who", "누가"), ("When", "언제"), ("Where", "어디서"), ("What", "무엇을"), ("How", "어떻게"), ("Why", "왜")):
            self.assertIn(f"<dt>{korean}<small>{english}</small>", markup)

    def test_action_cards_are_visually_and_semantically_distinct(self):
        with patch.object(app.st, "html") as html_renderer:
            app.render_launcher(app.get_projects())
        markup = html_renderer.call_args.args[0]
        self.assertIn("system-card project-node", markup)
        self.assertIn("is-action", markup)
        self.assertIn("card-action", markup)
        self.assertIn("새 탭에서 열기", markup)

    def test_governance_boundary_and_principles_todo_are_visible(self):
        with patch.object(app.st, "html") as html_renderer:
            app.render_launcher(app.get_projects())
        markup = html_renderer.call_args.args[0]
        self.assertIn("Ultra Brain 전용 거버넌스", markup)
        self.assertIn("현재 PRINCIPLES.md 원문을 유지합니다", markup)
        self.assertIn("공식 문서 확인 후 반영", markup)

    def test_enhancement_capability_modules_and_registry_are_rendered(self):
        with patch.object(app.st, "html") as html_renderer:
            app.render_launcher(app.get_projects())
        markup = html_renderer.call_args.args[0]
        for module in ("Analytics", "Learning", "Pattern Analysis", "Knowledge Management", "Optimization", "Rule Generation"):
            self.assertIn(module, markup)
        self.assertIn("v1.0.0 · 안정", markup)
        self.assertIn("v0.3.3", markup)

    def test_automation_capability_screen_modules_and_registry_are_rendered(self):
        with patch.object(app.st, "html") as html_renderer:
            app.render_launcher(app.get_projects())
        markup = html_renderer.call_args.args[0]
        for module in ("Workflow", "Scheduler", "Trigger", "Routine", "Auto Execution", "Auto Decision"):
            self.assertGreaterEqual(markup.count(module), 2)
        for stage in ("Validation", "Risk Check", "Approval", "Execution", "Logging", "Recovery"):
            self.assertIn(stage, markup)
        self.assertIn("v0.4.3", markup)

    def test_collaboration_connectivity_status_is_rendered_as_demo(self):
        with patch.object(app.st, "html") as html_renderer:
            app.render_launcher(app.get_projects())
        markup = html_renderer.call_args.args[0]
        for field in ("역량 버전", "등록된 연결 어댑터", "최근 상태 확인", "최근 연결 결과"):
            self.assertIn(field, markup)
        self.assertIn("메모리 내 연결 어댑터", markup)
        self.assertIn("v0.5.0", markup)

    def test_personal_secretary_status_and_registry_are_rendered(self):
        with patch.object(app.st, "html") as html_renderer:
            app.render_launcher(app.get_projects())
        markup = html_renderer.call_args.args[0]
        for field in ("오늘의 브리핑", "대기 중인 알림", "추천 생성", "알림 상태"):
            self.assertIn(field, markup)
        for function in ("일일 브리핑", "주간 검토", "월간 검토", "스마트 알림", "추천 엔진", "우선순위 관리", "결정 지원", "알림 관리"):
            self.assertIn(function, markup)
        self.assertIn("v0.6.0", markup)

    def test_redirect_techniques_are_not_used(self):
        source = Path(app.__file__).read_text(encoding="utf-8")
        for forbidden in ("st.switch_page", "meta http-equiv", "window.location", "share.streamlit.io"):
            self.assertNotIn(forbidden, source)

    def test_responsive_and_reduced_motion_contracts_exist(self):
        source = Path(app.__file__).read_text(encoding="utf-8")
        self.assertIn("@media(max-width:520px)", source)
        self.assertIn("@media(prefers-reduced-motion:reduce)", source)
        self.assertIn("grid-template-columns:1fr", source)

    def test_streamlit_home_runs_without_exception(self):
        app_test = AppTest.from_file(str(Path(app.__file__)), default_timeout=20)
        app_test.run()
        self.assertEqual(list(app_test.exception), [])

    def test_integrated_ai_hub_dashboard_runs_without_exception(self):
        app_test = AppTest.from_file(str(Path(app.__file__)), default_timeout=20)
        app_test.query_params["project"] = "ai-hub"
        app_test.run()
        self.assertEqual(list(app_test.exception), [])
        self.assertTrue(any(item.value == "운영 현황" for item in app_test.subheader))
        self.assertTrue(any("연결된 AI 제공자가 없습니다" in item.value for item in app_test.info))

    def test_concept_world_is_the_primary_interface(self):
        with patch.object(app.st, "html") as html_renderer:
            app.render_launcher(app.get_projects())
        markup = html_renderer.call_args.args[0]
        for identity in ("world-explorer", "world-tree-view", "세계수 ·", "열매 ·", "씨앗 ·", "GROWTH · 역량"):
            self.assertIn(identity, markup)
        self.assertIn('aria-label="OS 시스템 탐색 지도"', markup)

    def test_world_actions_explain_click_and_destination_before_navigation(self):
        cards = {item.name: app._project_node(item) for item in app.get_projects()}
        for name, card in cards.items():
            self.assertIn("클릭하여 이동", card, name)
            self.assertIn("card-action", card, name)
        self.assertIn("독립 앱 · 새 탭에서 열기", cards["Living OS"])
        self.assertIn("독립 앱 · 새 탭에서 열기", cards["Universal Learning Engine"])
        self.assertIn("OS Ecosystem 내부 · 현재 화면에서 열기", cards["AI Hub"])

    def test_world_landmark_and_actions_have_distinct_semantics(self):
        with patch.object(app.st, "html") as html_renderer:
            app.render_launcher(app.get_projects())
        markup = html_renderer.call_args.args[0]
        self.assertIn('<article class="system-card core-card world-core world-landmark">', markup)
        self.assertIn('<span class="interaction-hint is-current">현재 위치</span>', markup)
        self.assertEqual(markup.count('class="system-card project-node world-node'), 3)
        self.assertEqual(markup.count('data-destination='), 3)
        self.assertLess(markup.index('class="system-card project-node'), markup.index('class="system-card core-card'))

    def test_commercial_visual_restraint_avoids_generated_art_effects(self):
        source = Path(app.__file__).read_text(encoding="utf-8")
        self.assertNotIn("box-shadow:", source)
        self.assertNotIn("@keyframes", source)
        self.assertNotIn("animation:", source)
        contract = (Path(app.__file__).parent / "docs/architecture/UI_SYSTEM.md").read_text(encoding="utf-8")
        self.assertIn("code-native", contract)

    def test_ai_hub_uses_the_shared_seed_design_language(self):
        source = Path(app.__file__).read_text(encoding="utf-8")
        self.assertIn("platform-landmark", source)
        self.assertIn("내부 성장 시스템", source)
        self.assertIn("씨앗에서 성장하는 내부 시스템", source)


    def test_korean_ui_removes_english_first_release_placeholders(self):
        source = Path(app.__file__).read_text(encoding="utf-8")
        for placeholder in (
            "No eligible provider", "Dashboard Ready", "SYSTEM ONLINE",
            "INTERACTIVE SYSTEM MAP", "CONNECTION PENDING",
        ):
            self.assertNotIn(placeholder, source)
        for korean_label in ("자동 선택", "운영 화면 준비", "시스템 정상", "대화형 시스템 지도"):
            self.assertIn(korean_label, source)

    def test_common_empty_error_loading_and_performance_styles_exist(self):
        source = Path(app.__file__).read_text(encoding="utf-8")
        for selector in ('[data-testid="stAlert"]', '[data-testid="stSpinner"]', '[data-testid="stDataFrame"]'):
            self.assertIn(selector, source)
        self.assertIn("cursor:pointer", source)
        self.assertNotIn("fonts.googleapis.com", source)
        self.assertNotIn("backdrop-filter", source)
if __name__ == "__main__":
    unittest.main()
