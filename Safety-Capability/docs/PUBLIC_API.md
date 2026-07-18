# Public API and Boundary Contract

Safety Capability v1.0 exposes two supported public surfaces through the top-level
`safety_capability` package.

## Consumer surface

Modules may construct `SafetyExecutionContext` and `SafetyRequest`, call
`SafetyRuntime.execute()`, consume `SafetyResult`, and read capability health through
`SafetyRuntime.health_check()`. `ErrorCode`, `HealthReport`, and `HealthStatus` are
stable value contracts.

`execute()` accepts a `SafetyRequest` containing a `SafetyExecutionContext`. Passing a
different object is a caller programming error and raises `TypeError`. Once a valid
request object enters execution, validation, routing, component, and repository
failures are converted to a stable `SafetyResult` whenever a result can be formed.

## Extension and composition surface

`SafetyComponent`, `ComponentRegistry`, `ExecutionRepository`, and
`SQLiteExecutionRepository` are supported for composition roots and component or
storage adapter authors. Modules using the capability as consumers must not reach
through the runtime to mutate these collaborators during request processing.

`BasicValidationComponent` is a supported verification example, not a production
safety policy.

## Private surface

The `execution` implementation, SQLite schema, registry registration records, names
beginning with an underscore, and deep module imports not re-exported by the top-level
package are private implementation details. Consumers must not depend on them.

## Compatibility

The top-level names listed in `safety_capability.__all__`, request/result schemas,
error-code values, and documented extension contracts follow semantic versioning from
v1.0. Private implementation details may change without a major version increment.
