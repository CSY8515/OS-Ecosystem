# Personal Secretary Capability Guide

Create a `SecretaryContext` with a source, action, and dictionary payload, wrap it in `SecretaryRequest`, and execute it through `PersonalSecretaryService`. Supported actions are `daily_briefing`, `weekly_review`, `monthly_review`, `reminder`, `recommend`, `prioritize`, `decision_support`, `notify`, and `secretary`.

All results include success, status, message, version, details, timestamp, and a stable error code when unsuccessful. Invalid input is returned as `INPUT_VALIDATION_FAILED`; unknown actions use `ACTION_NOT_SUPPORTED`; rejected advice uses `SAFETY_REJECTED`.
