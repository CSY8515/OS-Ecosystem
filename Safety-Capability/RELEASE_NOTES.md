# Safety Capability v1.0.0 Release Notes

Status: Included stable capability in the OS Ecosystem v0.1.0 release candidate.

## Stable foundation

- Stable request, result, error, health, component, and repository contracts.
- Deterministic component registration and action routing.
- Isolated validation and component execution with controlled failure results.
- Replaceable execution repository with a SQLite adapter.
- Capability and per-component health reporting.
- Public, extension, and private boundary documentation.
- Artifact deployment and operational rollback contracts.

## Compatibility and scope

Python 3.11 or newer is required. v1.0 is synchronous and single-process. Runtime
rollback, production safety policies, module adapters, authentication, external
monitoring, automated intervention, and UI deployment are outside this release.

The capability package version is `1.0.0`. For this release, its artifacts and
checksums are published by the OS Ecosystem repository release tagged `v0.1.0`.
Repository and capability versions remain independent release identities.
