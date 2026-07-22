# OS Ecosystem v0.7.0 Release Notes

Status: Release Candidate
Target: Stable

## Outcome

v0.7.0 presents OS Ecosystem Core, AI Hub, Living OS, Universal Learning Engine, and five Capabilities as one coherent product without changing their ownership or deployment boundaries. Concept art is now the actual exploration interface, not a decorative layer around a conventional dashboard.

## Product experience

- Korean-first Header, Navigation, Breadcrumb, page titles, cards, lists, status, empty/error/loading language, and AI Hub operations
- official English System and module identifiers retained only as secondary labels where traceability requires them
- functional world model: Space is the shared environment, World Tree is the current Core, Fruit is an independent connected System, Seed is an internal growing System, branch is a route, and growth is Capability maturity
- clear Interaction Guide and full-card action language so a first-time user can identify clicks and destinations within three seconds
- compact first view on desktop and 390px mobile, with Action Nodes before the informational Core landmark in the narrow linear layout
- consistent actionable cards, buttons, empty/error/loading states, focus states, responsive layout, and reduced motion
- restrained code-native SVG/CSS without excessive glow, decoration, or animation
- local system-font stack, improved small-text contrast, and no render-blocking remote font request
- full-card direct external links for Living OS and Universal Learning Engine
- shared internal product shell and Seed language for AI Hub
- six-field Who, When, Where, What, How, Why explanations for every System and Capability
- portable common UI philosophy for Living OS, Universal Learning Engine, and Ultra Brain without transferring ownership or Governance

## Architecture and Governance

- formal OS System hierarchy and direct-child management rule
- authoritative Common UI System, Navigation Contract, and 6W Metadata Contract
- AI Hub remains a repository-owned component
- Living OS and Universal Learning Engine remain independent
- explicit Ultra Brain / OS Ecosystem Governance responsibility boundary
- current `PRINCIPLES.md` unchanged; official six operating principles registered as TODO

## Registry and Contract

Project, Capability, Version, Release, Contract, and Route Registries now use the same classifications and paths as the UI. Common UI, Metadata, and Navigation contracts are authoritative under `docs/architecture`.

## Validation

- Ecosystem and documentation: 42 passed
- Safety: 24 passed
- Enhancement: 5 passed
- Automation: 11 passed
- Collaboration & Connectivity: 26 passed
- Personal Secretary: 5 passed
- AI Hub: 64 passed
- Total: 177 passed (157 existing + 20 new)

Release publication was approved by the user on 2026-07-23. Production verification follows the approved Commit, Push, GitHub Release, and Streamlit Deploy sequence.
