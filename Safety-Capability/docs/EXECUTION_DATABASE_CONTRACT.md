# Execution Database Contract

`ExecutionRepository` is the storage abstraction. An adapter provides schema initialization, `save(record)`, `get(request_id)`, `list_records(limit)`, `count()`, and `close()`.

Each record contains the common result schema plus `source` and `target`: success/failure, status, error code, message, execution time, retry count, recovery result, version, timestamp, request ID, component ID, action, source, target, and JSON-compatible details.

SQLite is the v1.0 implementation. It uses a primary key on `request_id`, parameterized statements, JSON serialization for structured values, and a timestamp index. Business or policy logic must not be placed in a repository. `recovery_result` is `null` when recovery was not attempted or supported; it does not assert a successful rollback.
