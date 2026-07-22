from datetime import UTC, datetime
from pathlib import Path
import sqlite3

import pytest

from ai_hub.domain.executions import ExecutionAttempt, ExecutionSummary
from ai_hub.infrastructure.persistence import SQLiteExecutionRepository


NOW = datetime(2026, 7, 22, tzinfo=UTC)


def records():
    attempt = ExecutionAttempt("corr-1", 1, NOW, "openai", "model-1", "generation", 12.5, True)
    summary = ExecutionSummary(
        "corr-1", "request-1", "living-os", NOW, "generation", 12.5, True, 1, "v0.1",
        provider_id="openai", model_id="model-1", input_units=2, output_units=3, total_units=5,
    )
    return summary, (attempt,)


def test_repository_requires_explicit_migration(tmp_path: Path) -> None:
    repository = SQLiteExecutionRepository(tmp_path / "hub.sqlite3")
    summary, attempts = records()
    with pytest.raises(sqlite3.OperationalError):
        repository.record(summary, attempts)


def test_repository_records_summary_and_attempt_atomically(tmp_path: Path) -> None:
    repository = SQLiteExecutionRepository(tmp_path / "hub.sqlite3")
    repository.migrate()
    summary, attempts = records()
    repository.record(summary, attempts)
    assert repository.recent() == (summary,)
    assert repository.attempts_for("corr-1") == attempts


def test_schema_contains_no_raw_content_or_secret_columns(tmp_path: Path) -> None:
    repository = SQLiteExecutionRepository(tmp_path / "hub.sqlite3")
    repository.migrate()
    with sqlite3.connect(repository.database_path) as connection:
        schema = " ".join(row[0] for row in connection.execute(
            "SELECT sql FROM sqlite_master WHERE sql IS NOT NULL"
        ))
    lowered = schema.lower()
    for forbidden in ("prompt", "response_content", "api_key", "authorization", "secret"):
        assert forbidden not in lowered


def test_migration_is_idempotent(tmp_path: Path) -> None:
    repository = SQLiteExecutionRepository(tmp_path / "hub.sqlite3")
    repository.migrate()
    repository.migrate()
    with sqlite3.connect(repository.database_path) as connection:
        assert connection.execute("SELECT COUNT(*) FROM schema_migrations").fetchone()[0] == 1
