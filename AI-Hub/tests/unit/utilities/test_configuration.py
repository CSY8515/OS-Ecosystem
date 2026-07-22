from pathlib import Path

import pytest

from ai_hub.bootstrap.configuration import ConfigurationError, RuntimeConfiguration, load_secret_sources, secret_reference_for
from ai_hub.infrastructure.secrets import EnvironmentSecretResolver, SecretUnavailableError


def test_runtime_configuration_uses_safe_project_defaults(tmp_path: Path) -> None:
    config = RuntimeConfiguration.from_environment({}, project_root=tmp_path)
    assert config.data_path == (tmp_path / "data").resolve()
    assert config.database_path == (tmp_path / "data" / "ai_hub.sqlite3").resolve()
    assert not config.data_path.exists()


def test_runtime_configuration_rejects_unknown_log_level(tmp_path: Path) -> None:
    with pytest.raises(ConfigurationError):
        RuntimeConfiguration.from_environment({"AI_HUB_LOG_LEVEL": "verbose"}, project_root=tmp_path)


def test_secret_reference_is_stable_and_value_is_not_stored() -> None:
    reference = secret_reference_for("provider-openai")
    resolver = EnvironmentSecretResolver({reference: "secret-value"})
    assert reference == "AI_HUB_PROVIDER_OPENAI_API_KEY"
    assert resolver.resolve(reference) == "secret-value"


def test_missing_secret_error_exposes_reference() -> None:
    with pytest.raises(SecretUnavailableError, match="OPENAI_API_KEY"):
        EnvironmentSecretResolver({}).resolve("AI_HUB_OPENAI_API_KEY")


def test_secret_sources_do_not_override_environment(tmp_path: Path) -> None:
    (tmp_path / ".env").write_text("AI_HUB_OPENAI_API_KEY=file-value\nAI_HUB_GEMINI_MODEL='gemini-model'\n", encoding="utf-8")
    secret_dir = tmp_path / ".streamlit"
    secret_dir.mkdir()
    (secret_dir / "secrets.toml").write_text('AI_HUB_CLAUDE_API_KEY = "secret-value"\n', encoding="utf-8")
    values = load_secret_sources(tmp_path, {"AI_HUB_OPENAI_API_KEY": "environment-value"})
    assert values["AI_HUB_OPENAI_API_KEY"] == "environment-value"
    assert values["AI_HUB_GEMINI_MODEL"] == "gemini-model"
    assert values["AI_HUB_CLAUDE_API_KEY"] == "secret-value"
