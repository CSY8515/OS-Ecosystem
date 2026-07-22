# AI Hub v0.1 Data Contract

Status: Implemented candidate

AI Hub owns sanitized execution summaries, execution attempts, settings revisions, health observations, and derived usage evidence. Callers own prompts, responses, conversation history, and business records.

SQLite migrations are explicit and idempotent. Reads do not migrate storage. Execution records contain identifiers, timestamps, Provider, Model, Task, Duration, Success, stable Error, Retry, policy version, and normalized usage. They contain no raw prompt, raw response, API key, authorization header, or provider exception payload.

UTC-aware timestamps are required at domain boundaries. Unknown usage remains null rather than zero. Settings revisions are immutable.
