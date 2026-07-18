"""SQLite execution-record adapter."""
import json
import sqlite3
from pathlib import Path
from threading import RLock
from typing import Any
from safety_capability.core.result import SafetyResult
from .repository import ExecutionRepository
from .schema import CREATE_EXECUTIONS_TABLE, CREATE_TIMESTAMP_INDEX

class SQLiteExecutionRepository(ExecutionRepository):
    """Durable repository with no safety business logic."""
    def __init__(self, database_path: str | Path = ":memory:") -> None:
        self.database_path = str(database_path)
        if self.database_path != ":memory:":
            Path(self.database_path).parent.mkdir(parents=True, exist_ok=True)
        self._connection = sqlite3.connect(self.database_path, check_same_thread=False)
        self._connection.row_factory = sqlite3.Row
        self._lock = RLock()
        with self._lock, self._connection:
            self._connection.execute(CREATE_EXECUTIONS_TABLE)
            self._connection.execute(CREATE_TIMESTAMP_INDEX)

    def save(self, result: SafetyResult, *, source: str, target: str) -> None:
        values = result.to_dict()
        with self._lock, self._connection:
            self._connection.execute(
                """INSERT INTO executions
                (request_id, success, component_id, action, status, error_code, message,
                 execution_time, retry_count, recovery_result, capability_version, timestamp,
                 details, source, target)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (values["request_id"], int(values["success"]), values["component_id"], values["action"],
                 values["status"], values["error_code"], values["message"], values["execution_time"],
                 values["retry_count"], json.dumps(values["recovery_result"]), values["capability_version"],
                 values["timestamp"], json.dumps(values["details"]), source, target),
            )

    def _decode(self, row: sqlite3.Row) -> dict[str, Any]:
        record = dict(row)
        record["success"] = bool(record["success"])
        record["recovery_result"] = json.loads(record["recovery_result"])
        record["details"] = json.loads(record["details"])
        return record

    def get(self, request_id: str) -> dict[str, Any] | None:
        with self._lock:
            row = self._connection.execute("SELECT * FROM executions WHERE request_id = ?", (request_id,)).fetchone()
        return self._decode(row) if row else None

    def list_records(self, limit: int = 100) -> list[dict[str, Any]]:
        if limit < 1:
            raise ValueError("limit must be at least 1")
        with self._lock:
            rows = self._connection.execute(
                "SELECT * FROM executions ORDER BY timestamp DESC LIMIT ?", (limit,)
            ).fetchall()
        return [self._decode(row) for row in rows]

    def count(self) -> int:
        with self._lock:
            row = self._connection.execute("SELECT COUNT(*) AS total FROM executions").fetchone()
        return int(row["total"])

    def close(self) -> None:
        with self._lock:
            self._connection.close()

    def __enter__(self) -> "SQLiteExecutionRepository":
        return self

    def __exit__(self, *_: object) -> None:
        self.close()
