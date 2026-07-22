# AI Hub v0.1 Security

Status: Implementation baseline

- Real credentials are resolved at call time from environment-backed secret references.
- Provider and caller credentials are separate authorities.
- Caller scope is checked before routing.
- Router code imports no provider SDK.
- SDK errors are converted to safe codes before logging or return.
- Raw prompt and response content is not persisted by default.
- Configuration examples contain no real secrets.
- Live-provider tests are opt-in and require explicit authorization.

Before Release, complete dependency review, deployed transport authentication, credential rotation validation, access-log review, and authorized provider smoke checks.
