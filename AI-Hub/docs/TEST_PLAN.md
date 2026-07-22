# AI Hub v0.1 Test Plan

Status: Local plan complete

The default suite covers common configuration, redaction, Dashboard projections, three Provider adapter contracts, Health, Router gates and score, explicit SQLite migrations, Execution Log, Settings revisions, Usage Analytics, Usage Prediction, caller scopes, idempotency, retry/failover, recording failure, security boundaries, and operator startup.

Default verification uses fake clients and temporary databases. It must never require a real credential or paid call.

Release-only verification adds a clean optional-dependency installation, authorized live smoke call for each registered Provider model, supported Python CI, dependency/security review, and operator UI review. Live results do not replace deterministic contract tests.
