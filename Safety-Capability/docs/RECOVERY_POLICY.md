# Recovery and Rollback Policy

## Runtime rollback

Runtime rollback is not a mandatory Safety Capability v1.0 Core function. A generic
runtime cannot safely reverse module database changes, file writes, external API calls,
deployments, or other domain side effects without owning their transaction semantics.

The v1.0 runtime owns validation, failure isolation, optional retry, explicit results,
execution recording, and health reporting. Components and module adapters own
idempotency and compensating domain operations. A future, separately approved
`RecoveryStrategy` may opt in to compensation without changing this responsibility
boundary.

`SafetyResult.recovery_result` is `None` in v1.0 and means that recovery was not
attempted or is not supported. It must not be interpreted as a successful rollback.

## Deployment rollback

Deployment rollback is an operational release responsibility and is required. It
selects a previously verified immutable artifact and OS Ecosystem manifest entry; it
does not reverse a completed safety operation.

For the first Stable release, no previous Stable artifact exists. The v1.0 release
records `rollback_target: null`, documents removal or disablement and manifest
reversion, and proves that the exact v1.0 artifact can be reinstalled. Starting with
the next Stable release, verification must install the prior Stable artifact and pass
the runtime smoke and health checks.
