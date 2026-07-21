# Safety Capability v1.0 Master Design

## Purpose

Provide a stable, reusable safety execution foundation for multiple OS Ecosystem modules. v1.0 stabilizes the proven foundation contracts; it is not a complete safety product.

## Design goals

1. Independent package and runtime.
2. Interface-first, replaceable components and repositories.
3. Explicit success and failure results.
4. Failure isolation between components and requests.
5. Durable, queryable execution records.
6. Health visibility without module coupling.
7. Small functions, type hints, docstrings, and deterministic tests.

## Core model

- `SafetyExecutionContext`: caller-owned request data normalized into a common envelope.
- `SafetyRequest`: context plus an optional explicit component selection.
- `SafetyComponent`: pluggable validation/execution/health contract.
- `ComponentRegistry`: component catalog and enabled state.
- `SafetyExecutor`: validates and invokes exactly one selected component.
- `FailureIsolation`: converts exceptions into controlled execution outcomes.
- `SafetyResult`: stable response and persistence schema.
- `ExecutionRepository`: storage boundary; SQLite is the v1.0 adapter.
- `SafetyRuntime`: owns orchestration, timing, retries, and recording.

## Selection rules

An explicit `component_id` must exist, be enabled, and support the requested action. Without one, the registry deterministically chooses the first enabled supporting component by component ID. No implicit fallback occurs after a selected component fails.

## Failure semantics

Expected contract failures and unexpected component exceptions map to public error codes. Error messages are returned and recorded; execution failures do not cross the boundary after a valid `SafetyRequest` enters the runtime. Passing an object outside the documented public request type is a caller programming error and raises `TypeError`. A database write failure is returned as `REPOSITORY_ERROR`; the returned result preserves the original outcome even though that repository failure cannot itself be durably recorded.

## Recovery and deployment

Runtime rollback is not a v1.0 Core responsibility because the foundation does not own module transaction or compensation semantics. `recovery_result=None` means recovery was not attempted or supported. Deployment rollback is separate and selects a previously verified immutable release artifact and OS Ecosystem manifest entry. See `RECOVERY_POLICY.md` and `DEPLOYMENT_CONTRACT.md`.

## Evolution

Future versions can add routing policies, opt-in recovery strategies, async execution, external monitoring, stronger database delivery guarantees, and module adapters without changing component or result fundamentals.
