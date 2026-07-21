"""Synchronization lifecycle records without a distributed synchronization engine."""

from dataclasses import replace
from threading import RLock

from .enums import SyncStatus
from .models import SyncRecord, SyncRequest, utc_now


class SynchronizationManager:
    def __init__(self) -> None:
        self._records: dict[str, SyncRecord] = {}
        self._lock = RLock()

    def create(self, request: SyncRequest) -> SyncRecord:
        record = SyncRecord(request.sync_id, request.connector_id, request.source, request.target, utc_now(), metadata=dict(request.metadata))
        with self._lock:
            if record.sync_id in self._records:
                raise ValueError(f"sync already exists: {record.sync_id}")
            self._records[record.sync_id] = record
        return record

    def start(self, sync_id: str) -> SyncRecord:
        return self._update(sync_id, status=SyncStatus.RUNNING)

    def complete(self, sync_id: str, *, processed_count: int, success_count: int, failure_count: int = 0, conflict_count: int = 0) -> SyncRecord:
        if min(processed_count, success_count, failure_count, conflict_count) < 0:
            raise ValueError("sync counts cannot be negative")
        if success_count + failure_count > processed_count:
            raise ValueError("success_count + failure_count cannot exceed processed_count")
        if conflict_count:
            status = SyncStatus.CONFLICT
        elif failure_count and success_count:
            status = SyncStatus.PARTIAL
        elif failure_count:
            status = SyncStatus.FAILED
        else:
            status = SyncStatus.COMPLETED
        return self._update(sync_id, status=status, completed_at=utc_now(), processed_count=processed_count, success_count=success_count, failure_count=failure_count, conflict_count=conflict_count)

    def cancel(self, sync_id: str) -> SyncRecord:
        return self._update(sync_id, status=SyncStatus.CANCELLED, completed_at=utc_now())

    def get(self, sync_id: str) -> SyncRecord:
        try:
            return self._records[sync_id]
        except KeyError as exc:
            raise KeyError(f"sync not found: {sync_id}") from exc

    def _update(self, sync_id: str, **changes: object) -> SyncRecord:
        with self._lock:
            record = replace(self.get(sync_id), **changes)
            self._records[sync_id] = record
            return record
