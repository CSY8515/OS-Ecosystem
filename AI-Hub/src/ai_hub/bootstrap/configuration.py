from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Mapping
import os
import tomllib


class ConfigurationError(ValueError):
    """Raised when runtime configuration is unsafe or inconsistent."""


@dataclass(frozen=True, slots=True)
class RuntimeConfiguration:
    data_path: Path
    database_path: Path
    log_level: str = "INFO"

    @classmethod
    def from_environment(
        cls,
        environment: Mapping[str, str] | None = None,
        *,
        project_root: Path | None = None,
    ) -> "RuntimeConfiguration":
        values = os.environ if environment is None else environment
        root = (project_root or Path.cwd()).resolve()
        data_path = Path(values.get("AI_HUB_DATA_PATH", root / "data")).expanduser().resolve()
        database_path = Path(
            values.get("AI_HUB_DATABASE_PATH", data_path / "ai_hub.sqlite3")
        ).expanduser().resolve()
        log_level = values.get("AI_HUB_LOG_LEVEL", "INFO").strip().upper()
        if log_level not in {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}:
            raise ConfigurationError("AI_HUB_LOG_LEVEL is invalid")
        if database_path.is_dir():
            raise ConfigurationError("AI_HUB_DATABASE_PATH must identify a file")
        return cls(data_path=data_path, database_path=database_path, log_level=log_level)

    def prepare_local_data_path(self) -> None:
        self.data_path.mkdir(parents=True, exist_ok=True)


def secret_reference_for(provider_id: str) -> str:
    normalized = provider_id.strip().upper().replace("-", "_")
    if not normalized or not normalized.replace("_", "").isalnum():
        raise ConfigurationError("provider_id cannot form a safe secret reference")
    return f"AI_HUB_{normalized}_API_KEY"


def load_secret_sources(
    project_root: Path,
    environment: Mapping[str, str] | None = None,
) -> dict[str, str]:
    """Load environment, .env, and Streamlit secrets without overriding earlier values."""
    values = dict(os.environ if environment is None else environment)
    env_path = project_root / ".env"
    if env_path.is_file():
        for raw_line in env_path.read_text(encoding="utf-8").splitlines():
            line = raw_line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            name, value = line.split("=", 1)
            name = name.strip()
            if name.isidentifier():
                cleaned = value.strip()
                if len(cleaned) >= 2 and cleaned[0] == cleaned[-1] and cleaned[0] in {'"', "'"}:
                    cleaned = cleaned[1:-1]
                values.setdefault(name, cleaned)
    secrets_path = project_root / ".streamlit" / "secrets.toml"
    if secrets_path.is_file():
        document = tomllib.loads(secrets_path.read_text(encoding="utf-8"))
        for name, value in document.items():
            if isinstance(value, str):
                values.setdefault(name, value)
    return values
