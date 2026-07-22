from pathlib import Path


ROOT = Path(__file__).parents[2]


def test_router_has_no_provider_sdk_dependency() -> None:
    source = "\n".join(path.read_text(encoding="utf-8") for path in (ROOT / "src/ai_hub/domain/router").glob("*.py"))
    for forbidden in ("import openai", "import anthropic", "from google", "infrastructure.providers"):
        assert forbidden not in source


def test_source_contains_no_apparent_live_api_keys() -> None:
    source = "\n".join(path.read_text(encoding="utf-8", errors="ignore") for path in (ROOT / "src").rglob("*.py"))
    for prefix in ("sk-" + "proj-", "sk-" + "ant-", "AI" + "za"):
        assert prefix not in source
