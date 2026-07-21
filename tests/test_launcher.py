import os
import unittest
from unittest.mock import patch

import app


class LauncherContractTests(unittest.TestCase):
    def test_version_matches_release(self):
        self.assertEqual(app.VERSION, "0.3.3")

    def test_initial_catalog_contains_only_public_projects(self):
        projects = app.get_projects()
        self.assertEqual(
            [project.name for project in projects],
            ["Living OS", "Universal Learning Engine"],
        )

    def test_valid_environment_destination_is_accepted(self):
        with patch.dict(os.environ, {"ULE_URL": "https://ule.example.com"}, clear=False):
            self.assertEqual(app._configured_url("ULE_URL"), "https://ule.example.com")

    def test_unsafe_destination_is_rejected(self):
        with patch.dict(os.environ, {"ULE_URL": "javascript:alert(1)"}, clear=False):
            self.assertIsNone(app._configured_url("ULE_URL"))

    def test_missing_destination_renders_pending_node(self):
        project = app.Project("Example", "EXAMPLE", "Description", None, "node-left")
        rendered = app._project_node(project)
        self.assertIn("CONNECTION PENDING", rendered)
        self.assertNotIn("href=", rendered)

    def test_connected_destination_is_html_escaped(self):
        project = app.Project(
            "Example", "EXAMPLE", "Description", "https://example.com/?a=1&b=2", "node-left"
        )
        rendered = app._project_node(project)
        self.assertIn("a=1&amp;b=2", rendered)

    def test_connected_destination_opens_directly_in_new_tab(self):
        project = app.Project(
            "Example", "EXAMPLE", "Description", "https://example.com/app", "node-left"
        )
        rendered = app._project_node(project)
        self.assertIn('href="https://example.com/app"', rendered)
        self.assertIn('target="_blank"', rendered)
        self.assertIn('rel="noopener noreferrer"', rendered)
        self.assertNotIn("share.streamlit.io", rendered)



    def test_ecosystem_hierarchy_menu_and_sections_are_rendered(self):
        projects = (
            app.Project("Living OS", "LIVING", "Living", "https://living.example.com", "node-left"),
            app.Project("Universal Learning Engine", "LEARNING", "Learning", "https://learning.example.com", "node-right"),
        )
        with patch.object(app.st, "html") as html_renderer:
            app.render_launcher(projects)

        markup = html_renderer.call_args.args[0]
        for menu in ("Projects", "Capability", "Governance", "Architecture", "Registry"):
            self.assertIn(f">{menu}</a>", markup)
        for section_id in ("capability", "governance", "architecture", "registry"):
            self.assertIn(f'id="{section_id}"', markup)
        for item in (
            "Ecosystem Constitution",
            "Ecosystem Rules",
            "Ecosystem Principles",
            "Ecosystem Standards",
            "Ecosystem Policies",
            "Master Architecture",
            "Repository Strategy",
            "Integration Strategy",
            "Roadmap",
            "Capability Architecture",
            "Project Registry",
            "Capability Registry",
            "Release History",
        ):
            self.assertIn(item, markup)

    def test_enhancement_capability_modules_and_registry_are_rendered(self):
        with patch.object(app.st, "html") as html_renderer:
            app.render_launcher(app.get_projects())
        markup = html_renderer.call_args.args[0]
        self.assertGreaterEqual(markup.count("Enhancement Capability"), 2)
        for module in ("Analytics", "Learning", "Pattern Analysis", "Knowledge Management", "Optimization", "Rule Generation"):
            self.assertIn(module, markup)
        self.assertIn("v1.0.0 · STABLE", markup)
        self.assertIn("v0.3.3", markup)

if __name__ == "__main__":
    unittest.main()
