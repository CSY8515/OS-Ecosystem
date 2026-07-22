from pathlib import Path
import re
import unittest
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
DOC_CATEGORIES = ("architecture", "governance", "registry", "release", "capabilities")
CAPABILITY_READMES = (
    ROOT / "Safety-Capability" / "README.md",
    ROOT / "Enhancement-Capability" / "README.md",
    ROOT / "Automation-Capability" / "README.md",
    ROOT / "Collaboration-Connectivity-Capability" / "README.md",
    ROOT / "Personal-Secretary-Capability" / "README.md",
)
LINK_PATTERN = re.compile(r"\[[^\]]+\]\(([^)]+)\)")


class DocumentationStructureTests(unittest.TestCase):
    def test_authoritative_categories_and_files_exist(self):
        for category in DOC_CATEGORIES:
            self.assertTrue((ROOT / "docs" / category).is_dir(), category)

        required = (
            "docs/README.md",
            "docs/architecture/ARCHITECTURE.md",
            "docs/architecture/MASTER_DESIGN.md",
            "docs/architecture/ROADMAP.md",
            "docs/architecture/STRUCTURE.md",
            "docs/governance/CONSTITUTION.md",
            "docs/governance/RULES.md",
            "docs/governance/STANDARDS.md",
            "docs/governance/POLICIES.md",
            "docs/registry/PROJECT_REGISTRY.md",
            "docs/registry/CAPABILITY_REGISTRY.md",
            "docs/registry/VERSION_REGISTRY.md",
            "docs/registry/RELEASE_REGISTRY.md",
            "docs/release/RELEASE_NOTES_v0.5.0.md",
            "docs/release/RELEASE_NOTES_v0.6.0.md",
            "docs/release/RELEASE_NOTES_v0.6.1.md",
            "docs/release/VERSION_HISTORY.md",
            "docs/release/MIGRATION_NOTES_v0.4.4.md",
            "docs/capabilities/safety/README.md",
            "docs/capabilities/enhancement/README.md",
            "docs/capabilities/automation/README.md",
            "docs/capabilities/collaboration-connectivity/README.md",
            "docs/capabilities/collaboration-connectivity/CONNECTOR_CONTRACT.md",
            "docs/capabilities/collaboration-connectivity/IMPORT_EXPORT_CONTRACT.md",
            "docs/capabilities/collaboration-connectivity/MESSAGING_CONTRACT.md",
            "docs/capabilities/collaboration-connectivity/SYNCHRONIZATION_CONTRACT.md",
            "docs/capabilities/collaboration-connectivity/ERROR_CODE_REFERENCE.md",
            "docs/capabilities/collaboration-connectivity/SECURITY_CONSIDERATIONS.md",
            "docs/capabilities/collaboration-connectivity/INTEGRATION_GUIDE.md",
            "docs/capabilities/personal-secretary/README.md",
            "docs/capabilities/personal-secretary/ARCHITECTURE.md",
            "docs/capabilities/personal-secretary/MASTER_DESIGN.md",
            "docs/capabilities/personal-secretary/CAPABILITY_GUIDE.md",
            "docs/capabilities/personal-secretary/RECOMMENDATION_GUIDE.md",
            "docs/capabilities/personal-secretary/REMINDER_GUIDE.md",
            "docs/capabilities/personal-secretary/DECISION_SUPPORT_GUIDE.md",
            "docs/capabilities/personal-secretary/INTEGRATION_CONTRACT.md",
            "docs/capabilities/personal-secretary/RELEASE_NOTES.md",
            "docs/capabilities/personal-secretary/CHANGELOG.md",
        )
        for relative in required:
            self.assertTrue((ROOT / relative).is_file(), relative)

    def test_root_design_documents_have_moved(self):
        for filename in (
            "ARCHITECTURE.md",
            "MASTER_DESIGN.md",
            "ROADMAP.md",
            "STRUCTURE.md",
            "RELEASE_NOTES.md",
        ):
            self.assertFalse((ROOT / filename).exists(), filename)

    def test_release_identity_is_consistent(self):
        self.assertEqual((ROOT / "VERSION").read_text(encoding="utf-8").strip(), "0.6.1")
        app_source = (ROOT / "app.py").read_text(encoding="utf-8")
        self.assertIn('VERSION = "0.6.1"', app_source)
        self.assertIn("OS Ecosystem v0.6.1", app_source)
        self.assertIn("v0.6.1", (ROOT / "README.md").read_text(encoding="utf-8"))

    def test_capability_readmes_link_to_central_docs(self):
        expected = ("safety", "enhancement", "automation", "collaboration-connectivity", "personal-secretary")
        for readme, capability in zip(CAPABILITY_READMES, expected):
            content = readme.read_text(encoding="utf-8")
            self.assertIn(f"../docs/capabilities/{capability}/", content)

    def test_internal_markdown_links_resolve(self):
        markdown_files = [ROOT / "README.md", *CAPABILITY_READMES]
        markdown_files.extend(sorted((ROOT / "docs").rglob("*.md")))
        failures = []

        for document in markdown_files:
            content = document.read_text(encoding="utf-8")
            for raw_target in LINK_PATTERN.findall(content):
                target = raw_target.strip().strip("<>")
                if target.startswith(("http://", "https://", "mailto:", "#")):
                    continue
                target = unquote(target.split("#", 1)[0])
                if not target:
                    continue
                resolved = (document.parent / target).resolve()
                if not resolved.exists():
                    failures.append(f"{document.relative_to(ROOT)} -> {raw_target}")

        self.assertEqual(failures, [], "\n".join(failures))


if __name__ == "__main__":
    unittest.main()
