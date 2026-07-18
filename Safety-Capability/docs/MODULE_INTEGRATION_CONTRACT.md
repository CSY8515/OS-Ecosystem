# Module Integration Contract

## Allowed flow

```text
Module -> SafetyExecutionContext -> SafetyRequest -> SafetyRuntime.execute()
       <- SafetyResult
```

A module creates a context and request, calls the public runtime, and consumes the result. It may use `success`, `status`, `error_code`, `message`, and `details` for its own decisions.

## Boundary rules

- Modules must not change Safety Capability source code to integrate.
- Modules must not access registry, executor, repository, or component internals.
- Safety Capability does not own or implement module business logic.
- Module-specific payload schemas belong in separately installed components or adapters.
- `source` and `target` identify the caller and intended scope; they do not create imports between projects.

No real module adapter is included in v1.0.
