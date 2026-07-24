# Changelog

All notable OS Ecosystem changes are recorded here. Releases follow semantic versioning and Git tags.

## [0.7.1] - Unreleased

### Changed

- Replaced the black card-dashboard composition with a restrained World Atlas inside the OS Ecosystem Fruit.
- Locked the supplied world composition as the official blueprint and refined only foliage, terrain, dome construction, material, and lighting quality.
- Locked the supplied world composition as the official blueprint and refined only foliage, terrain, dome construction, material, and lighting quality.
- Added the official `Universe → Ultra Brain → Meta OS → OS Ecosystem → Project → Subsystem → Module → Capability → Engine` world hierarchy.
- Represented Living OS, Universal Learning Engine, and AI Hub as exactly three Dome Project Seeds, each containing its own sapling and ecosystem.
- Kept the official English product brands while making visible functions and guidance Korean-first.
- Replaced duplicate top navigation and internal card grids with one orientation bar and one world navigation surface containing only the three Projects.
- Removed 6W and destination metadata attributes from Home markup while retaining their authoritative Architecture and Registry contracts.
- Removed 6W and destination metadata attributes from Home markup while retaining their authoritative Architecture and Registry contracts.
- Reflowed the same world into a vertical, touch-safe route map at 390px instead of scaling down the desktop composition.
- Unified AI Hub with the Project Seed language while preserving its internal route and existing operational behavior.

### Preserved

- Preserved v0.7.0 Architecture, Registry, Contract, Governance responsibility boundaries, 6W Metadata, Capability behavior, and all existing Routes.
- Preserved direct new-tab links to Living OS and Universal Learning Engine.
- Preserved `docs/governance/PRINCIPLES.md` unchanged.

### Validation

- Added 19 UI contract tests on top of the existing 177-test baseline, including official key-visual ownership and semantic-navigation coverage.
- Release publication and production deployment remain blocked until the user approves the actual Desktop and 390px Mobile renders.

## [0.7.0] - 2026-07-23

### Added

- Added shared Common UI System, 6W Metadata, Navigation, Route, Contract, and Governance responsibility contracts.
- Added complete 6W explanations for connected Systems and Capabilities.
- Added semantic World Tree, Fruit, Seed, branch, and growth-axis interface components.
- Added Korean-first AI Hub metrics and an actionable empty state.
- Added v0.7.0 product, documentation, link, accessibility, and boundary regression tests.

### Changed

- Unified the home and AI Hub Header, Navigation, Breadcrumb, card, button, and state language.
- Completed a Korean-first visible-copy audit for titles, actions, lists, statuses, Empty state, and AI Hub operations.
- Moved Action Nodes before the informational Core landmark in the narrow linear layout and compacted the first mobile viewport.
- Removed the remote font request and increased small-text contrast without adding glow or decorative motion.
- Made concept art the primary interface while keeping click actions, destinations, focus states, and ownership visually explicit.
- Replaced decorative glow and motion with restrained code-native SVG/CSS world landmarks and action nodes.
- Classified OS Ecosystem Core, AI Hub, Living OS, and Universal Learning Engine consistently across Architecture, UI, and Registry.
- Kept Living OS and Universal Learning Engine as independent connected Systems using direct public application links.
- Standardized Architecture, Governance, Registry, README, and version identity for v0.7.0.

### Governance

- Preserved `docs/governance/PRINCIPLES.md` unchanged.
- Registered the separate official six operating principles as a non-blocking TODO.
- Kept Ultra Brain-only Governance outside OS Ecosystem operating authority.

### Validation

- Passed the existing 157 tests and 20 new v0.7.0 tests: 177 total.
- GitHub Actions, deployment, and production verification remain pending user approval and publication.

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
