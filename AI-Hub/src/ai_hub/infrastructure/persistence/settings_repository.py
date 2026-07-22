from __future__ import annotations

from dataclasses import asdict
from datetime import datetime
from pathlib import Path
import json
import sqlite3

from ai_hub.domain.settings import HubSettings, SettingsRevision


class SQLiteSettingsRepository:
    def __init__(self, database_path: Path | str) -> None:
        self.database_path = Path(database_path)

    def migrate(self) -> None:
        self.database_path.parent.mkdir(parents=True, exist_ok=True)
        with sqlite3.connect(self.database_path) as connection:
            connection.execute("""
                CREATE TABLE IF NOT EXISTS settings_revisions (
                    revision_id TEXT PRIMARY KEY,
                    created_at TEXT NOT NULL,
                    actor_id TEXT NOT NULL,
                    settings_json TEXT NOT NULL
                )
            """)
            connection.execute("CREATE INDEX IF NOT EXISTS idx_settings_time ON settings_revisions(created_at DESC)")

    def add(self, revision: SettingsRevision) -> None:
        payload = json.dumps(asdict(revision.settings), sort_keys=True, separators=(",", ":"))
        with sqlite3.connect(self.database_path) as connection:
            connection.execute(
                "INSERT INTO settings_revisions VALUES (?, ?, ?, ?)",
                (revision.revision_id, revision.created_at.isoformat(), revision.actor_id, payload),
            )

    def current(self) -> SettingsRevision | None:
        with sqlite3.connect(self.database_path) as connection:
            row = connection.execute(
                "SELECT revision_id, created_at, actor_id, settings_json FROM settings_revisions ORDER BY created_at DESC, revision_id DESC LIMIT 1"
            ).fetchone()
        if row is None:
            return None
        return SettingsRevision(row[0], datetime.fromisoformat(row[1]), row[2], HubSettings(**json.loads(row[3])))

    def history(self) -> tuple[SettingsRevision, ...]:
        with sqlite3.connect(self.database_path) as connection:
            rows = connection.execute(
                "SELECT revision_id, created_at, actor_id, settings_json FROM settings_revisions ORDER BY created_at, revision_id"
            ).fetchall()
        return tuple(SettingsRevision(row[0], datetime.fromisoformat(row[1]), row[2], HubSettings(**json.loads(row[3]))) for row in rows)
