# Synchronization Contract

Version: v1.0.0

`SyncRequest` identifies a connector, source, target, item set, metadata, and sync ID. `SyncRecord` tracks start/completion time, status, processed/success/failure/conflict counts, error code, and metadata.

Statuses are `PENDING`, `RUNNING`, `COMPLETED`, `PARTIAL`, `FAILED`, `CONFLICT`, and `CANCELLED`.

v1.0 records and validates lifecycle state only. It does not implement real-time bidirectional synchronization, multi-server coordination, automatic conflict resolution, or durable scheduling. Projects own comparison keys, conflict policy, canonical state, and recovery decisions.
