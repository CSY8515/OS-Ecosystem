# Changelog

## 1.0.0 - 2026-07-18

### Stable

- Promoted the proven Safety Capability foundation contracts to the v1.0 public API.
- Defined consumer, extension, and private boundaries.
- Isolated invalid component health reports and tightened request routing validation.
- Defined runtime recovery scope, artifact deployment, and deployment rollback policy.

### Explicitly not included

- Runtime rollback or automatic recovery strategies.
- Direct OS module integrations, production safety policies, authentication, external monitoring, automated intervention, or UI deployment.

## 0.1.0 - 2026-07-18

### Added

- Independent Safety Capability package and public contracts.
- Component registry with discovery, version, state, and health information.
- Failure-isolated execution runtime with stable results and optional retries.
- Replaceable execution repository and SQLite adapter.
- Basic validation test component, executable example, automated tests, and architecture documentation.

### Explicitly not included

- OS module integrations, production safety policies, external deployment, monitoring services, authentication, automatic recovery, or UI.
