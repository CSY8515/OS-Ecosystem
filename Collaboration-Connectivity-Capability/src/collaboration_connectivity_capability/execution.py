"""Sanitized connection execution records and aggregate Enhancement inputs."""

from __future__ import annotations

from collections import Counter
from threading import RLock

from .models import CollaborationConnectivityExecutionRecord

SENSITIVE_KEYS = frozenset({"authorization", "api_key", "apikey", "token", "password", "secret", "credential"})


def sanitize_metadata(metadata: dict[str, object]) -> dict[str, object]:
    return {key: "[REDACTED]" if key.lower() in SENSITIVE_KEYS else value for key, value in metadata.items()}


class ExecutionRecorder:
    def __init__(self) -> None:
        self._records: list[CollaborationConnectivityExecutionRecord] = []
        self._lock = RLock()

    def record(self, record: CollaborationConnectivityExecutionRecord) -> None:
        with self._lock:
            self._records.append(record)

    def all(self) -> tuple[CollaborationConnectivityExecutionRecord, ...]:
        return tuple(self._records)

    def recent(self, limit: int = 20) -> tuple[CollaborationConnectivityExecutionRecord, ...]:
        return tuple(self._records[-max(0, limit):])

    def analytics(self) -> dict[str, object]:
        total = len(self._records)
        successes = sum(record.success for record in self._records)
        durations = [record.execution_time_ms for record in self._records]
        errors = Counter(record.error_code for record in self._records if record.error_code)
        by_connector: dict[str, dict[str, int]] = {}
        by_operation: dict[str, dict[str, int]] = {}
        for record in self._records:
            for bucket, key in ((by_connector, record.connector_id), (by_operation, record.operation)):
                stats = bucket.setdefault(key, {"total": 0, "success": 0, "failure": 0})
                stats["total"] += 1
                stats["success" if record.success else "failure"] += 1
        provider_stability = {key: values["success"] / values["total"] for key, values in by_connector.items()}
        sync_records = [record for record in self._records if record.operation in {"sync", "sync_data", "synchronize"}]
        return {
            "total_executions": total,
            "success_rate": successes / total if total else 0.0,
            "average_response_time_ms": sum(durations) / total if total else 0.0,
            "connector_performance": by_connector,
            "provider_stability": provider_stability,
            "operation_performance": by_operation,
            "repeated_errors": dict(errors),
            "sync_success_rate": sum(record.success for record in sync_records) / len(sync_records) if sync_records else 0.0,
        }
