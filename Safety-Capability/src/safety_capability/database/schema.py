"""SQLite schema for common execution records."""
CREATE_EXECUTIONS_TABLE = """
CREATE TABLE IF NOT EXISTS executions (
    request_id TEXT PRIMARY KEY,
    success INTEGER NOT NULL,
    component_id TEXT NOT NULL,
    action TEXT NOT NULL,
    status TEXT NOT NULL,
    error_code TEXT,
    message TEXT NOT NULL,
    execution_time REAL NOT NULL,
    retry_count INTEGER NOT NULL,
    recovery_result TEXT,
    capability_version TEXT NOT NULL,
    timestamp TEXT NOT NULL,
    details TEXT NOT NULL,
    source TEXT NOT NULL,
    target TEXT NOT NULL
)
"""
CREATE_TIMESTAMP_INDEX = "CREATE INDEX IF NOT EXISTS idx_executions_timestamp ON executions(timestamp)"
