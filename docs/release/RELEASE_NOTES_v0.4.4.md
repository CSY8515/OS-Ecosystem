# OS Ecosystem v0.4.4 Release Notes

Status: Stable
Release type: Documentation Structure Standardization Patch

## Summary

v0.4.4 establishes docs as the authoritative home for Architecture, Governance, Registry, Release, and Capability documentation. This release changes document placement, indexes, and links only; product and capability behavior remain unchanged.

## Included

- Standardized docs/architecture, docs/governance, docs/registry, docs/release, and docs/capabilities categories.
- Moved Architecture, Master Design, Roadmap, and Structure documents into docs/architecture.
- Added the complete Governance set under docs/governance.
- Added Project, Capability, Version, and Release registries under docs/registry.
- Added release notes, version history, and migration notes under docs/release.
- Consolidated Safety, Enhancement, and Automation documentation under docs/capabilities.
- Updated repository and capability README links to the authoritative locations.
- Added automated documentation-structure and internal-link validation.
- Added a GitHub Actions regression workflow for the ecosystem and all capability suites.

## Compatibility

- Launcher layout, menus, project cards, and direct external-link behavior are unchanged.
- Living OS and Universal Learning Engine production destinations are unchanged.
- Safety, Enhancement, and Automation package APIs and runtime behavior are unchanged.
- No migration is required for application users. Documentation maintainers should use the [migration notes](./MIGRATION_NOTES_v0.4.4.md).

## Validation

- Repository documentation structure and README contract checked.
- Internal Markdown links checked.
- Streamlit application startup checked.
- Ecosystem and capability regression suites checked.
- GitHub Actions and production deployment verified after publication.

## Release identity

- Repository: OS Ecosystem
- Version and tag: v0.4.4
- Previous version: v0.4.3
- Production: https://8javbq85jtappi6tkdhkt7g.streamlit.app/

See [Version History](./VERSION_HISTORY.md) and the [Release Registry](../registry/RELEASE_REGISTRY.md).
