# Changelog

All notable OS Ecosystem changes are recorded here. Releases follow semantic versioning and Git tags.

## [0.6.2] - 2026-07-22

### Added

- Included the complete AI Hub v0.1.0 common-platform component under `AI-Hub/`.
- Added the repository-internal AI Hub operator route at `?project=ai-hub`.
- Added AI Hub installation and tests to the repository CI workflow.
- Added explicit ignore rules for AI Hub secrets and runtime data.

### Changed

- Corrected AI Hub ownership from an independent project/service assumption to an OS Ecosystem-owned common platform component.
- Updated architecture, structure, registry, roadmap, approval, review, and operations documents.
- Updated the launcher card, top navigation, and registry status to the integrated model.

### Removed

- Removed `AI_HUB_URL` and the external AI Hub dashboard fallback.
- Removed independent AI Hub repository, release, service, tag, and deployment assumptions.

### Security

- Kept Provider keys, `.env` variants, Streamlit secrets, databases, logs, caches, coverage, and runtime data outside Git.

## [0.6.1] - 2026-07-22

- Added the initial AI Hub launcher card, menu entry, and project overview. Ownership and release-boundary descriptions were corrected in v0.6.2.
