import os
import re
import unittest
from pathlib import Path
from unittest.mock import patch

import app
from streamlit.testing.v1 import AppTest


class LauncherContractTests(unittest.TestCase):
    def launcher_markup(self) -> str:
        with patch.object(app.st, "markdown") as html_renderer:
            app.render_launcher(app.get_projects())
        return html_renderer.call_args.args[0]

    def test_version_matches_release(self):
        self.assertEqual(app.VERSION, "0.7.1")

    def test_initial_catalog_contains_official_systems(self):
        self.assertEqual(
            [project.name for project in app.get_projects()],
            ["Living OS", "Universal Learning Engine", "AI Hub"],
        )

    def test_ai_hub_uses_repository_internal_dashboard(self):
        project = next(item for item in app.get_projects() if item.name == "AI Hub")
        self.assertEqual(project.url, "?project=ai-hub")
        rendered = app._project_node(project)
        self.assertIn('href="./?project=ai-hub"', rendered)
        self.assertIn('target="_self"', rendered)
        self.assertNotIn('target="_blank"', rendered)

    def test_valid_environment_destination_is_accepted(self):
        with patch.dict(os.environ, {"ULE_URL": "https://ule.example.com"}, clear=False):
            self.assertEqual(app._configured_url("ULE_URL"), "https://ule.example.com")

    def test_unsafe_destination_is_rejected(self):
        with patch.dict(os.environ, {"ULE_URL": "javascript:alert(1)"}, clear=False):
            self.assertIsNone(app._configured_url("ULE_URL"))

    def test_missing_destination_renders_unavailable_state(self):
        rendered = app._project_node(
            app.Project("Example", "예시 기능", "Description", None, "node-living")
        )
        self.assertIn("연결 준비 중", rendered)
        self.assertIn("is-unavailable", rendered)
        self.assertNotIn("href=", rendered)

    def test_connected_destination_is_html_escaped(self):
        project = app.Project(
            "Example", "예시 기능", "Description", "https://example.com/?a=1&b=2", "node-living"
        )
        self.assertIn("a=1&amp;b=2", app._project_node(project))

    def test_connected_destination_opens_directly_in_new_tab(self):
        rendered = app._project_node(
            app.Project("Example", "예시 기능", "Description", "https://example.com/app", "node-living")
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

    def test_korean_first_orientation_and_breadcrumb(self):
        markup = app._product_header_markup("Home")
        self.assertIn("OS Ecosystem", markup)
        self.assertIn("현재 위치", markup)
        self.assertIn("생태계 중심", markup)
        self.assertIn("홈", markup)
        self.assertIn('class="location-path breadcrumb"', markup)
        self.assertIn('aria-current="page"', markup)

    def test_main_world_contains_projects_only(self):
        markup = self.launcher_markup()
        self.assertIn('id="projects"', markup)
        self.assertEqual(markup.count('class="project-seed '), 3)
        for forbidden_id in (
            "ai-hub", "capability", "cap-safety", "cap-enhancement",
            "automation", "connectivity", "secretary", "governance", "architecture", "registry",
        ):
            self.assertNotIn(f'id="{forbidden_id}"', markup)
        for forbidden_label in ("공통 기능", "운영 기준", "시스템 구조", "시스템 정보"):
            self.assertNotIn(forbidden_label, markup)

    def test_ai_hub_is_rendered_only_as_a_project_seed(self):
        markup = self.launcher_markup()
        self.assertIn('href="./?project=ai-hub"', markup)
        self.assertIn("AI Hub</strong>", markup)
        self.assertIn("AI 운영</em>", markup)
        self.assertNotIn("OpenAI · Gemini · Claude", markup)
        self.assertNotIn('id="ai-hub"', markup)

    def test_every_system_and_capability_has_complete_six_w_metadata(self):
        values = [app.get_project_metadata(item) for item in app.get_projects()]
        values.extend(item.metadata for item in app.get_capabilities())
        for metadata in values:
            self.assertTrue(
                all(getattr(metadata, name).strip() for name in ("who", "when", "where", "what", "how", "why"))
            )
        markup = app._six_w_markup(values[0])
        for korean, english in (
            ("누가", "Who"), ("언제", "When"), ("어디서", "Where"),
            ("무엇을", "What"), ("어떻게", "How"), ("왜", "Why"),
        ):
            self.assertIn(f"<dt>{korean}<small>{english}</small>", markup)

    def test_action_nodes_are_visually_and_semantically_distinct(self):
        markup = self.launcher_markup()
        self.assertEqual(markup.count('class="project-seed '), 3)
        self.assertIn("world-action", markup)
        self.assertIn("새 탭에서 열기", markup)
        self.assertNotIn("map-node seed-node", markup)
        self.assertNotIn("root-node", markup)

    def test_governance_boundary_is_not_exposed_on_main_world(self):
        markup = self.launcher_markup()
        self.assertNotIn("Governance", markup)
        self.assertNotIn("PRINCIPLES.md", markup)
        boundary = Path("docs/governance/RESPONSIBILITY_BOUNDARY.md").read_text(encoding="utf-8")
        self.assertIn("Ultra Brain", boundary)

    def test_enhancement_capability_is_not_exposed_on_main_world(self):
        markup = self.launcher_markup()
        for module in ("분석", "학습", "패턴", "지식", "최적화", "규칙"):
            self.assertNotIn(f"<li>{module}</li>", markup)
        self.assertNotIn("Enhancement Capability", markup)

    def test_automation_capability_is_not_exposed_on_main_world(self):
        markup = self.launcher_markup()
        for module in ("작업 흐름", "일정", "조건", "반복", "자동 실행", "결정 지원"):
            self.assertNotIn(f"<li>{module}</li>", markup)
        self.assertNotIn("검증→승인→실행→기록", markup)

    def test_collaboration_connectivity_is_not_exposed_on_main_world(self):
        markup = self.launcher_markup()
        self.assertNotIn("독립 시스템 사이의 교환과 동기화", markup)
        self.assertNotIn("데모 · v1.0.0", markup)

    def test_personal_secretary_is_not_exposed_on_main_world(self):
        markup = self.launcher_markup()
        for function in ("브리핑", "검토", "알림", "추천", "우선순위", "결정"):
            self.assertNotIn(f"<li>{function}</li>", markup)
        self.assertNotIn("다음 행동을 이해하기 쉽게 제안", markup)

    def test_redirect_techniques_are_not_used(self):
        source = Path(app.__file__).read_text(encoding="utf-8")
        for forbidden in ("st.switch_page", "meta http-equiv", "window.location", "share.streamlit.io"):
            self.assertNotIn(forbidden, source)

    def test_responsive_and_reduced_motion_contracts_exist(self):
        source = Path(app.__file__).read_text(encoding="utf-8")
        self.assertIn("@media(max-width:700px)", source)
        self.assertIn("@media(prefers-reduced-motion:reduce)", source)
        self.assertIn("overflow-x:hidden", source)
        self.assertIn("min-height:68px", source)

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
        markup = self.launcher_markup()
        for identity in (
            "official-world", "world-stage", "ecosystem-key-visual",
            "OS Ecosystem 열매 안의 우주와 세 개의 프로젝트 씨앗",
        ):
            self.assertIn(identity, markup)
        self.assertEqual(markup.count('class="project-seed '), 3)

    def test_world_actions_explain_destination_before_navigation(self):
        nodes = {item.name: app._project_node(item) for item in app.get_projects()}
        self.assertIn("실생활 운영", nodes["Living OS"])
        self.assertIn("범용 학습 엔진", nodes["Universal Learning Engine"])
        self.assertIn("AI 운영", nodes["AI Hub"])
        self.assertIn("새 탭에서 열기", nodes["Living OS"])
        self.assertIn("새 탭에서 열기", nodes["Universal Learning Engine"])
        self.assertIn("현재 화면에서 열기", nodes["AI Hub"])

    def test_world_landmark_and_actions_have_distinct_semantics(self):
        markup = self.launcher_markup()
        self.assertIn('class="core-signature core-action is-selected"', markup)
        self.assertNotIn("현재 세계", markup)
        self.assertIn('aria-current="location"', markup)
        self.assertEqual(markup.count('class="project-seed '), 3)
        self.assertNotIn("data-destination=", markup)
        core = markup.split('class="core-signature core-action is-selected"', 1)[1].split("</a>", 1)[0]
        self.assertIn('href="./?view=overview"', core)
        self.assertIn('target="_self"', core)
        self.assertIn("전체 보기", core)

    def test_parent_world_labels_are_not_exposed_on_home(self):
        markup = self.launcher_markup()
        for parent in ("Universe", "Ultra Brain", "Meta OS"):
            self.assertNotIn(parent, markup)
        self.assertNotIn('class="world-lineage"', markup)
        self.assertIn("OS Ecosystem", markup)

    def test_all_projects_are_seeds_containing_saplings(self):
        for project in app.get_projects():
            node = app._project_node(project)
            self.assertIn("project-seed", node)
            self.assertIn("프로젝트 씨앗", node)
            self.assertIn("mobile-seed-art", node)
            self.assertNotIn("sapling-node", node)

    def test_capabilities_are_not_main_world_project_seeds(self):
        markup = self.launcher_markup()
        self.assertNotIn('class="seed-dome"', markup)
        self.assertNotIn("map-node seed-node", markup)
        self.assertNotIn("Capability", markup)

    def test_ecosystem_fruit_is_the_navigation_world_boundary(self):
        markup = self.launcher_markup()
        self.assertIn("OS Ecosystem 열매 안의 우주", markup)
        self.assertIn('class="world-stage"', markup)
        self.assertIn('class="ecosystem-key-visual"', markup)

    def test_interaction_states_are_explicit_and_restrained(self):
        source = Path(app.__file__).read_text(encoding="utf-8")
        for state in (
            ":hover", ":focus-visible", ":active", "is-selected",
            'aria-current="location"', "transition:", "prefers-reduced-motion",
        ):
            self.assertIn(state, source)
        for forbidden in ("@keyframes", "animation:"):
            self.assertNotIn(forbidden, source)
        self.assertIn("transition-duration:.08s", source)

    def test_commercial_visual_restraint_avoids_generated_art_effects(self):
        source = Path(app.__file__).read_text(encoding="utf-8")
        for forbidden in ("@keyframes", "animation:", "filter:drop-shadow", "backdrop-filter", "box-shadow:0 0"):
            self.assertNotIn(forbidden, source)
        self.assertLessEqual(source.count("box-shadow:"), 4)
        self.assertLessEqual(source.count("linear-gradient"), 2)

    def test_ai_hub_uses_the_shared_sapling_and_seed_design_language(self):
        source = Path(app.__file__).read_text(encoding="utf-8")
        node = app._project_node(next(item for item in app.get_projects() if item.name == "AI Hub"))
        self.assertIn("project-seed", node)
        self.assertIn("프로젝트 씨앗", node)
        self.assertIn("sapling-chamber", source)
        self.assertIn("sapling-emblem", source)
        self.assertIn("묘목 · 내부 프로젝트", source)
        self.assertIn("subsystem-seeds", source)
        self.assertIn("AI Hub 내부 돔형 씨앗", source)
        self.assertIn("OS Ecosystem / AI Hub", source)
        self.assertNotIn(".integrated-platform{min-height:100vh", source)

    def test_korean_ui_minimizes_developer_terms_in_primary_labels(self):
        markup = self.launcher_markup()
        for label in ("현재 위치", "홈", "실생활 운영", "범용 학습 엔진", "AI 운영"):
            self.assertIn(label, markup)
        for removed in ("현재 세계", "Universe", "Ultra Brain", "Meta OS"):
            self.assertNotIn(removed, markup)
        for tag in ("h1", "h2", "h3", "strong", "b"):
            for rejected in ("Capability", "Registry", "Contract"):
                self.assertNotIn(f"<{tag}>{rejected}</{tag}>", markup)

    def test_common_empty_error_loading_and_performance_styles_exist(self):
        source = Path(app.__file__).read_text(encoding="utf-8")
        for selector in ('[data-testid="stAlert"]', '[data-testid="stDataFrame"]'):
            self.assertIn(selector, source)
        self.assertIn("cursor:pointer", source)
        self.assertNotIn("fonts.googleapis.com", source)

    # v0.7.1 UI Patch acceptance tests
    def test_top_text_menu_is_removed_in_favor_of_world_navigation(self):
        markup = self.launcher_markup()
        self.assertNotIn("ecosystem-nav", markup)
        self.assertNotIn("Home</small>", markup)
        self.assertIn("orientation-bar", markup)

    def test_desktop_atlas_exposes_every_primary_click_area(self):
        markup = self.launcher_markup()
        for class_name in ("node-living", "node-learning", "node-ai"):
            self.assertIn(class_name, markup)
        for forbidden in ("seed-safety", "seed-growth", "root-governance", "root-architecture", "root-registry"):
            self.assertNotIn(forbidden, markup)

    def test_world_nodes_map_to_existing_routes(self):
        markup = self.launcher_markup()
        for route in (
            "./?view=overview",
            "https://living-os-h5uinmvmjpvv6m8phat28a.streamlit.app/",
            "https://universal-learning-engine-zb5aezuadeu84gnqust8mw.streamlit.app/",
            "./?project=ai-hub",
        ):
            self.assertIn(f'href="{route}"', markup)
        for forbidden in ("#cap-safety", "#governance", "#architecture", "#registry"):
            self.assertNotIn(f'href="{forbidden}"', markup)

    def test_mobile_world_map_has_semantic_layer_order(self):
        source = Path(app.__file__).read_text(encoding="utf-8")
        for rule in (
            ".official-world .ecosystem-key-visual{position:relative;inset:auto;order:1",
            ".project-seed-field{position:relative;inset:auto;order:2",
            ".project-seed .mobile-seed-art{position:absolute;display:block",
        ):
            self.assertIn(rule, source)

    def test_mobile_touch_targets_meet_minimum_size(self):
        source = Path(app.__file__).read_text(encoding="utf-8")
        mobile = source.rsplit("@media(max-width:700px)", 1)[1]
        self.assertIn("min-height:68px", source)
        self.assertIn("min-height:274px", mobile)
        self.assertIn("min-height:240px", mobile)
        self.assertIn("width:100%", mobile)

    def test_official_answer_asset_and_mobile_seed_derivatives_are_used(self):
        self.assertEqual(app.KEY_VISUAL_PATH.name, "os-ecosystem-official-answer-v071-final-key-visual.png")
        expected = {
            "Living OS": "living-os-official-v071-final.png",
            "Universal Learning Engine": "universal-learning-engine-official-v071-final.png",
            "AI Hub": "ai-hub-official-v071-final.png",
        }
        for project, filename in expected.items():
            self.assertEqual(app.PROJECT_SEED_ART[project].name, filename)
            self.assertTrue(app.PROJECT_SEED_ART[project].is_file())

    def test_project_seed_labels_remain_short_and_action_is_shape_native(self):
        for project in app.get_projects():
            node = app._project_node(project)
            label = node.split('<span class="project-seed-label">', 1)[1].split("</span>", 1)[0]
            self.assertIn(f"<strong>{project.name}</strong>", label)
            self.assertIn(f"<em>{project.label}</em>", label)
            self.assertNotIn("새 탭에서 열기", label)
            self.assertNotIn("현재 화면에서 열기", label)

    def test_official_world_has_no_instructional_or_internal_feature_copy(self):
        markup = self.launcher_markup()
        visible_markup = re.sub(r'src="data:image/png;base64,[^"]+"', 'src=""', markup)
        for forbidden in (
            "세계수에서 탐색하세요",
            "프로젝트를 선택하세요",
            "씨앗을 클릭하세요",
            "재무",
            "건강",
            "차량",
            "주거",
            "식사",
            "학습 시작",
            "CBT",
            "복습",
            "케이스북",
            "분석",
        ):
            self.assertNotIn(forbidden, visible_markup)

    def test_mobile_world_is_recomposed_as_seed_map(self):
        source = Path(app.__file__).read_text(encoding="utf-8")
        mobile = source.rsplit("@media(max-width:700px)", 1)[1]
        self.assertIn("grid-template-columns:repeat(2,minmax(0,1fr))", mobile)
        self.assertIn(".project-seed.node-ai{grid-column:1/-1", mobile)
        self.assertIn("aspect-ratio:455/690", mobile)
        self.assertIn("aspect-ratio:470/441", mobile)

    def test_rejected_dashboard_card_classes_are_removed(self):
        source = Path(app.__file__).read_text(encoding="utf-8")
        for rejected in ("system-card", "capability-card", "info-card", "status-grid", "capability-grid"):
            self.assertNotIn(rejected, source)

    def test_official_brand_names_are_not_translated(self):
        markup = self.launcher_markup()
        for brand in ("OS Ecosystem", "Living OS", "Universal Learning Engine", "AI Hub"):
            self.assertIn(brand, markup)
        for parent_brand in ("Universe", "Ultra Brain", "Meta OS"):
            self.assertNotIn(parent_brand, markup)
        for translated_brand in ("생활 운영체제", "보편 학습 엔진", "초지능 두뇌"):
            self.assertNotIn(translated_brand, markup)

    def test_orientation_component_exposes_current_location_and_home(self):
        home = app._orientation_markup("Home")
        ai_hub = app._orientation_markup("AI Hub")
        overview = app._orientation_markup("Overview")
        self.assertIn('aria-current="page"', home)
        self.assertNotIn('aria-current="page"', ai_hub)
        self.assertIn("OS Ecosystem · 생태계 중심", home)
        self.assertIn("AI Hub · AI 운영", ai_hub)
        self.assertIn("OS Ecosystem · 전체 보기", overview)
        self.assertIn('aria-label="홈으로 돌아가기"', ai_hub)

    def test_ecosystem_overview_is_an_internal_clickable_route(self):
        markup = self.launcher_markup()
        self.assertIn('href="./?view=overview"', markup)
        self.assertIn('aria-label="OS Ecosystem Overview 현재 화면에서 열기"', markup)
        with patch.object(app.st, "markdown") as html_renderer:
            app.render_ecosystem_overview()
        overview = html_renderer.call_args.args[0]
        self.assertIn("OS Ecosystem Overview", overview)
        self.assertIn("OS Ecosystem / Overview", overview)
        self.assertIn('href="./"', overview)
        self.assertIn("세계로 돌아가기", overview)

    def test_world_nodes_have_icons_and_accessible_names(self):
        markup = self.launcher_markup()
        for name in (
            "Living OS 프로젝트 씨앗, 새 탭에서 열기",
            "Universal Learning Engine 프로젝트 씨앗, 새 탭에서 열기",
            "AI Hub 프로젝트 씨앗, 현재 화면에서 열기",
        ):
            self.assertIn(f'aria-label="{name}"', markup)

    def test_six_w_metadata_stays_out_of_main_markup(self):
        markup = self.launcher_markup()
        for field in ("data-who=", "data-when=", "data-where=", "data-what=", "data-how=", "data-why="):
            self.assertNotIn(field, markup)
        self.assertNotIn('<details class="context-drawer">', markup)
        self.assertNotIn("6하 원칙 보기", markup)

    def test_shared_visual_language_combines_key_visual_and_semantic_ui(self):
        source = Path(app.__file__).read_text(encoding="utf-8")
        self.assertIn("def _icon_svg", source)
        self.assertIn("KEY_VISUAL_PATH", source)
        self.assertIn("_key_visual_data_uri", source)
        self.assertIn('<img class="ecosystem-key-visual"', source)
        self.assertIn('alt="" aria-hidden="true"', source)
        self.assertNotIn("background-image:url", source)

    def test_official_key_visual_is_project_owned_png(self):
        self.assertTrue(app.KEY_VISUAL_PATH.is_file())
        payload = app.KEY_VISUAL_PATH.read_bytes()
        self.assertTrue(payload.startswith(b"\x89PNG\r\n\x1a\n"))
        self.assertGreater(len(payload), 1_000_000)

    def test_key_visual_does_not_replace_accessible_navigation_labels(self):
        markup = self.launcher_markup()
        self.assertIn('aria-label="OS Ecosystem 열매 안의 우주와 세 개의 프로젝트 씨앗"', markup)
        self.assertIn('aria-current="location"', markup)
        for label in ("Living OS", "Universal Learning Engine", "AI Hub"):
            self.assertIn(label, markup)

    def test_secrets_and_runtime_details_are_not_rendered(self):
        markup = self.launcher_markup()
        for forbidden in ("API_KEY", "TOKEN", "DATABASE_URL", "st.secrets", "execution_repository"):
            self.assertNotIn(forbidden, markup)
        self.assertIn("인증 정보와 원문 데이터는 표시하지 않습니다", Path(app.__file__).read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
