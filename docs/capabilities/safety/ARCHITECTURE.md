# Safety Capability Architecture

## Position in the OS Ecosystem

```text
User
  -> Ultra Brain
    -> Meta OS
      -> OS Ecosystem
        -> Capability Layer
          -> Safety Capability
        -> Module Layer
          -> Living OS / Universal Learning Engine / future modules
```

Safety Capability belongs to the Capability Layer. It is above the Module Layer and is independently deployable and testable. Modules consume its public request/result contract; they do not import or mutate its internal registry, executor, database, or component implementation.

The supported consumer, extension, and private surfaces are defined in `PUBLIC_API.md`. Composition roots may configure documented component and repository abstractions; ordinary module consumers use only the request, runtime, result, error, and health contracts.

## Runtime flow

```text
SafetyRequest
  -> context validation
  -> registered component selection
  -> enabled/action checks
  -> isolated component execution
  -> output validation
  -> execution-record persistence
  -> SafetyResult
```

Every completed request produces the same `SafetyResult` shape for success and failure. Component exceptions are contained by the execution boundary. The registry and runtime remain available after one component fails.

## Internal boundaries

- `core`: stable request, context, result, errors, health, and runtime orchestration.
- `interfaces`: replaceable component contract.
- `registry`: thread-safe registration, discovery, state, version, and health access.
- `execution`: component invocation and exception isolation.
- `database`: replaceable execution-record repository plus SQLite adapter.
- `components`: test/example components only; no module-specific safety policy.

## Dependency direction

The core depends on abstractions (`SafetyComponent`, `ExecutionRepository`) rather than concrete module logic or a specific storage engine. SQLite is an outer adapter. Components never access runtime internals or the database directly.

## v1.0 constraints

This foundation does not integrate Living OS, Universal Learning Engine, Investment OS, Job OS, authentication, monitoring services, AI risk analysis, automatic blocking/recovery, or a user interface.

Runtime rollback is not owned by the Core. Operational deployment rollback pins immutable GitHub Release artifacts and manifest entries. Safety Capability deployment is artifact publication and clean-install verification, not a Streamlit or service deployment.
