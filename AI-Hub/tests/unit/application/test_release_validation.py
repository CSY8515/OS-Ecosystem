from ai_hub.bootstrap.release_validation import build_preflight_report


def test_release_preflight_reports_presence_without_secret_values() -> None:
    values = {
        "AI_HUB_OPENAI_API_KEY": "openai-secret",
        "AI_HUB_OPENAI_MODEL": "openai-model",
        "AI_HUB_GEMINI_API_KEY": "gemini-secret",
        "AI_HUB_GEMINI_MODEL": "gemini-model",
        "AI_HUB_CLAUDE_API_KEY": "claude-secret",
        "AI_HUB_CLAUDE_MODEL": "claude-model",
    }
    report = build_preflight_report(values)
    assert report["ready"] is True
    assert report["keys_ready"] is True
    assert report["models_ready"] is True
    rendered = repr(report)
    assert "openai-secret" not in rendered
    assert "gemini-secret" not in rendered
    assert "claude-secret" not in rendered


def test_release_preflight_requires_all_keys_and_models() -> None:
    report = build_preflight_report({})
    assert report["ready"] is False
    assert report["keys_ready"] is False
    assert report["models_ready"] is False
    assert all(not item["ready"] for item in report["providers"])


def test_release_preflight_allows_key_first_model_discovery() -> None:
    report = build_preflight_report({
        "AI_HUB_OPENAI_API_KEY": "secret",
        "AI_HUB_GEMINI_API_KEY": "secret",
        "AI_HUB_CLAUDE_API_KEY": "secret",
    })
    assert report["keys_ready"] is True
    assert report["models_ready"] is False
    assert report["ready"] is False
