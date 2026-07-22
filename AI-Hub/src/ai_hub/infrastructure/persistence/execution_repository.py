from __future__ import annotations

from datetime import datetime
from pathlib import Path
import sqlite3

from ai_hub.domain.executions import ExecutionAttempt, ExecutionSummary


SCHEMA_VERSION = 1


class SQLiteExecutionRepository:
    def __init__(self, database_path: Path | str) -> None:
        self.database_path = Path(database_path)

    def migrate(self) -> None:
        self.database_path.parent.mkdir(parents=True, exist_ok=True)
        with sqlite3.connect(self.database_path) as connection:
            connection.execute("PRAGMA foreign_keys = ON")
            connection.executescript("""
                CREATE TABLE IF NOT EXISTS schema_migrations (
                    version INTEGER PRIMARY KEY,
                    applied_at TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS execution_summaries (
                    correlation_id TEXT PRIMARY KEY,
                    request_id TEXT NOT NULL,
                    caller_id TEXT NOT NULL,
                    timestamp TEXT NOT NULL,
                    task_kind TEXT NOT NULL,
                    duration_ms REAL NOT NULL,
                    success INTEGER NOT NULL,
                    attempt_count INTEGER NOT NULL,
                    routing_policy_version TEXT NOT NULL,
                    provider_id TEXT,
                    model_id TEXT,
                    error_code TEXT,
                    input_units INTEGER,
                    output_units INTEGER,
                    total_units INTEGER
                );
                CREATE TABLE IF NOT EXISTS execution_attempts (
                    correlation_id TEXT NOT NULL,
                    sequence INTEGER NOT NULL,
                    timestamp TEXT NOT NULL,
                    provider_id TEXT NOT NULL,
                    model_id TEXT NOT NULL,
                    task_kind TEXT NOT NULL,
                    duration_ms REAL NOT NULL,
                    success INTEGER NOT NULL,
                    error_code TEXT,
                    retry INTEGER NOT NULL,
                    PRIMARY KEY (correlation_id, sequence),
                    FOREIGN KEY (correlation_id) REFERENCES execution_summaries(correlation_id)
                );
                CREATE INDEX IF NOT EXISTS idx_execution_time ON execution_summaries(timestamp DESC);
                CREATE INDEX IF NOT EXISTS idx_execution_provider ON execution_summaries(provider_id, timestamp DESC);
            """)
            connection.execute(
                "INSERT OR IGNORE INTO schema_migrations(version, applied_at) VALUES (?, ?)",
                (SCHEMA_VERSION, datetime.now().astimezone().isoformat()),
            )

    def record(self, summary: ExecutionSummary, attempts: tuple[ExecutionAttempt, ...]) -> None:
        if len(attempts) != summary.attempt_count:
            raise ValueError("attempt count does not match summary")
        if any(item.correlation_id != summary.correlation_id for item in attempts):
            raise ValueError("attempt correlation does not match summary")
        with sqlite3.connect(self.database_path) as connection:
            connection.execute("PRAGMA foreign_keys = ON")
            connection.execute(
                "INSERT INTO execution_summaries VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (
                    summary.correlation_id, summary.request_id, summary.caller_id, summary.timestamp.isoformat(),
                    summary.task_kind, summary.duration_ms, int(summary.success), summary.attempt_count,
                    summary.routing_policy_version, summary.provider_id, summary.model_id, summary.error_code,
                    summary.input_units, summary.output_units, summary.total_units,
                ),
            )
            connection.executemany(
                "INSERT INTO execution_attempts VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                [(
                    item.correlation_id, item.sequence, item.timestamp.isoformat(), item.provider_id,
                    item.model_id, item.task_kind, item.duration_ms, int(item.success), item.error_code,
                    int(item.retry),
                ) for item in attempts],
            )

    def recent(self, limit: int = 100) -> tuple[ExecutionSummary, ...]:
        if limit <= 0 or limit > 1000:
            raise ValueError("limit must be between 1 and 1000")
        with sqlite3.connect(self.database_path) as connection:
            rows = connection.execute(
                "SELECT * FROM execution_summaries ORDER BY timestamp DESC LIMIT ?", (limit,)
            ).fetchall()
        return tuple(ExecutionSummary(
            correlation_id=row[0], request_id=row[1], caller_id=row[2], timestamp=datetime.fromisoformat(row[3]),
            task_kind=row[4], duration_ms=row[5], success=bool(row[6]), attempt_count=row[7],
            routing_policy_version=row[8], provider_id=row[9], model_id=row[10], error_code=row[11],
            input_units=row[12], output_units=row[13], total_units=row[14],
        ) for row in rows)

    def attempts_for(self, correlation_id: str) -> tuple[ExecutionAttempt, ...]:
        with sqlite3.connect(self.database_path) as connection:
            rows = connection.execute(
                "SELECT * FROM execution_attempts WHERE correlation_id = ? ORDER BY sequence", (correlation_id,)
            ).fetchall()
        return tuple(ExecutionAttempt(
            correlation_id=row[0], sequence=row[1], timestamp=datetime.fromisoformat(row[2]),
            provider_id=row[3], model_id=row[4], task_kind=row[5], duration_ms=row[6],
            success=bool(row[7]), error_code=row[8], retry=bool(row[9]),
        ) for row in rows)
