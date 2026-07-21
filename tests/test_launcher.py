import os
import unittest
from unittest.mock import patch

import app


class LauncherContractTests(unittest.TestCase):
    def test_version_matches_release(self):
        self.assertEqual(app.VERSION, "0.2.1")

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


if __name__ == "__main__":
    unittest.main()
