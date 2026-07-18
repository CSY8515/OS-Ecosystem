# v1.0 Release Checklist

## Architecture and documentation

- [x] Runtime rollback and deployment rollback responsibilities are separate.
- [x] Artifact deployment and clean-install verification are documented.
- [x] Consumer, extension, and private API boundaries are documented.
- [x] No module-specific logic or direct OS module integration exists.
- [x] README, Master Design, contracts, roadmap, changelog, and release notes identify v1.0.
- [x] Runtime database files, environments, caches, secrets, and build outputs are ignored.

## Validation

- [x] Automated tests pass locally (24 tests on 2026-07-18).
- [x] Public contract and error-boundary tests pass.
- [x] Example runtime execution, persistence readback, and health checks pass.
- [x] Wheel and source distribution preflight builds succeed.
- [x] The preflight wheel installs and runs outside the source tree.
- [x] Preflight artifact contents contain no secrets or machine-specific paths.

## Controlled release

- [ ] Commit scope reviewed and approved.
- [ ] Conventional Commit created.
- [ ] Push reviewed and approved.
- [ ] Component tag `safety-capability/v1.0.0` created.
- [ ] Draft GitHub Release contains artifacts, checksums, and release notes.
- [ ] Deployment and rollback-readiness checks pass.
- [ ] GitHub Release published as Stable.
- [ ] Release Report completed.
