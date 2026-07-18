# Safety Component Interface Contract

Every component implements `SafetyComponent` and exposes:

- `component_id`: stable, unique, non-empty identifier.
- `component_name`: human-readable name.
- `version`: component version string.
- `supported_actions`: immutable action names.
- `validate_input(context)`: raises a typed error for invalid input.
- `execute(context)`: performs one requested action and returns a dictionary.
- `validate_output(output, context)`: raises for invalid component output.
- `health_check()`: returns a `HealthReport`; it must not mutate runtime state.
- `metadata()`: returns JSON-compatible descriptive data.

The capability may call these methods multiple times. Components must not depend on a particular module, database adapter, UI, or registry implementation. Unhandled component exceptions are allowed but are converted to `EXECUTION_FAILED` at the isolation boundary. A health exception or a non-`HealthReport` return is isolated as `UNKNOWN` health.

Input and output are deliberately generic in v1.0: module data stays inside `context.payload` and component results stay inside `SafetyResult.details`.
