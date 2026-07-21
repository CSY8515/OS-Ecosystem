# Deployment Contract

Safety Capability is an internal Python foundation. It has no Streamlit, service, or
operator-UI deployment. Deployment is complete only when an immutable GitHub Release
artifact is proven consumable.

## Release identity

- Package version: `1.0.0`
- Component tag: `safety-capability/v1.0.0`
- The tag, package metadata, changelog, and release notes identify the same version.

## Artifact gate

1. Build wheel and source distribution from the approved tag.
2. Record SHA-256 checksums for both artifacts.
3. Attach the artifacts and checksums to a draft GitHub Release.
4. Install the wheel into a clean supported Python environment without the source tree.
5. Verify import, public version, normal execution, persistence readback, controlled
   error handling, and capability/component health.
6. Confirm the rollback policy and release-manifest fields.
7. Publish the GitHub Release as Stable only after every check passes.

## Required evidence

The Release Report records the commit, tag, artifact names and hashes, Python version,
test results, smoke-test result, health result, rollback target, and final release URL.
An OS Ecosystem manifest must pin the exact version, full commit SHA, artifact hash,
contract version, verification status, and deployment status.
