from pathlib import Path
import hashlib
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
            "docs/architecture/METADATA_CONTRACT.md",
            "docs/architecture/UI_SYSTEM.md",
            "docs/architecture/NAVIGATION_CONTRACT.md",
            "docs/architecture/ROADMAP.md",
            "docs/architecture/STRUCTURE.md",
            "docs/governance/CONSTITUTION.md",
            "docs/governance/RULES.md",
            "docs/governance/PRINCIPLES.md",
            "docs/governance/STANDARDS.md",
            "docs/governance/POLICIES.md",
            "docs/governance/RESPONSIBILITY_BOUNDARY.md",
            "docs/registry/PROJECT_REGISTRY.md",
            "docs/registry/CAPABILITY_REGISTRY.md",
            "docs/registry/VERSION_REGISTRY.md",
            "docs/registry/RELEASE_REGISTRY.md",
            "docs/registry/CONTRACT_REGISTRY.md",
            "docs/registry/ROUTE_REGISTRY.md",
            "docs/release/RELEASE_NOTES_v0.5.0.md",
            "docs/release/RELEASE_NOTES_v0.6.0.md",
            "docs/release/RELEASE_NOTES_v0.6.1.md",
            "docs/release/RELEASE_NOTES_v0.6.2.md",
            "docs/release/RELEASE_NOTES_v0.7.0.md",
            "docs/release/RELEASE_REVIEW_v0.7.0.md",
            "docs/release/RELEASE_NOTES_v0.7.1.md",
            "docs/release/RELEASE_REVIEW_v0.7.1.md",
            "docs/release/VERSION_HISTORY.md",
            "CHANGELOG.md",
            "AI-Hub/README.md",
            "AI-Hub/docs/MASTER_DESIGN.md",
            "docs/capabilities/safety/README.md",
            "docs/capabilities/enhancement/README.md",
            "docs/capabilities/automation/README.md",
            "docs/capabilities/collaboration-connectivity/README.md",
            "docs/capabilities/personal-secretary/README.md",
        )
        for relative in required:
            self.assertTrue((ROOT / relative).is_file(), relative)

    def test_root_design_documents_have_moved(self):
        for filename in ("ARCHITECTURE.md", "MASTER_DESIGN.md", "ROADMAP.md", "STRUCTURE.md", "RELEASE_NOTES.md"):
            self.assertFalse((ROOT / filename).exists(), filename)

    def test_release_identity_is_consistent(self):
        self.assertEqual((ROOT / "VERSION").read_text(encoding="utf-8").strip(), "0.7.1")
        app_source = (ROOT / "app.py").read_text(encoding="utf-8")
        self.assertIn('VERSION = "0.7.1"', app_source)
        self.assertIn("OS Ecosystem v0.7.1", app_source)
        self.assertIn("v0.7.1", (ROOT / "README.md").read_text(encoding="utf-8"))

    def test_ai_hub_is_integrated_and_external_url_is_not_supported(self):
        source = (ROOT / "app.py").read_text(encoding="utf-8")
        self.assertNotIn("AI_HUB_URL", source)
        self.assertIn('"?project=ai-hub"', source)
        self.assertTrue((ROOT / "AI-Hub" / "src" / "ai_hub").is_dir())

    def test_architecture_declares_official_system_hierarchy(self):
        content = (ROOT / "docs/architecture/ARCHITECTURE.md").read_text(encoding="utf-8")
        for item in ("OS Ecosystem Core", "AI Hub v0.1.0", "Living OS v2.0.4", "Universal Learning Engine v1.0.0"):
            self.assertIn(item, content)
        self.assertIn("각 계층은 직접 하위 계약만 관리합니다", content)

    def test_principles_source_is_unchanged_and_todo_is_registered(self):
        principles = ROOT / "docs/governance/PRINCIPLES.md"
        normalized_source = principles.read_bytes().replace(b"\r\n", b"\n")
        self.assertEqual(
            hashlib.sha256(normalized_source).hexdigest(),
            "9b1d06e967b45e3cf68b1bf57449a984c35d7c7bb20993672034cb6bd306e613",
        )
        roadmap = (ROOT / "docs/architecture/ROADMAP.md").read_text(encoding="utf-8")
        boundary = (ROOT / "docs/governance/RESPONSIBILITY_BOUNDARY.md").read_text(encoding="utf-8")
        self.assertIn("공식 ‘6대 운영 원칙’", roadmap)
        self.assertIn("does not block v0.7.0", boundary)

    def test_governance_responsibility_boundary_is_explicit(self):
        content = (ROOT / "docs/governance/RESPONSIBILITY_BOUNDARY.md").read_text(encoding="utf-8")
        self.assertIn("Ultra Brain boundary", content)
        self.assertIn("OS Ecosystem responsibility", content)
        self.assertIn("Connected project autonomy", content)

    def test_registry_and_contract_routes_are_consistent(self):
        projects = (ROOT / "docs/registry/PROJECT_REGISTRY.md").read_text(encoding="utf-8")
        routes = (ROOT / "docs/registry/ROUTE_REGISTRY.md").read_text(encoding="utf-8")
        contracts = (ROOT / "docs/registry/CONTRACT_REGISTRY.md").read_text(encoding="utf-8")
        self.assertIn("?project=ai-hub", projects)
        self.assertIn("target=_blank", routes)
        self.assertIn("6W Metadata", contracts)
        self.assertIn("Navigation", contracts)

    def test_capability_readmes_link_to_central_docs(self):
        expected = ("safety", "enhancement", "automation", "collaboration-connectivity", "personal-secretary")
        for readme, capability in zip(CAPABILITY_READMES, expected):
            self.assertIn(f"../docs/capabilities/{capability}/", readme.read_text(encoding="utf-8"))


    def test_common_ui_system_is_portable_without_crossing_governance(self):
        content = (ROOT / "docs/architecture/UI_SYSTEM.md").read_text(encoding="utf-8")
        for meaning in ("World Tree", "Fruit", "Project Seed", "Sapling", "Growth"):
            self.assertIn(meaning, content)
        self.assertIn("exactly three Project Seeds", content)
        self.assertIn("do not appear on Home", content)
        self.assertIn("Living OS, Universal Learning Engine, Meta OS, and Ultra Brain", content)
        self.assertIn("does not transfer Repository ownership or Governance authority", content)

    def test_internal_markdown_links_resolve(self):
        markdown_files = [ROOT / "README.md", *CAPABILITY_READMES]
        markdown_files.extend(sorted((ROOT / "docs").rglob("*.md")))
        markdown_files.append(ROOT / "AI-Hub" / "README.md")
        markdown_files.extend(sorted((ROOT / "AI-Hub" / "docs").rglob("*.md")))
        failures = []
        for document in markdown_files:
            content = document.read_text(encoding="utf-8")
            for raw_target in LINK_PATTERN.findall(content):
                target = raw_target.strip().strip("<>")
                if target.startswith(("http://", "https://", "mailto:", "#")):
                    continue
                target = unquote(target.split("#", 1)[0])
                if target and not (document.parent / target).resolve().exists():
                    failures.append(f"{document.relative_to(ROOT)} -> {raw_target}")
        self.assertEqual(failures, [], "\n".join(failures))


if __name__ == "__main__":
    unittest.main()
