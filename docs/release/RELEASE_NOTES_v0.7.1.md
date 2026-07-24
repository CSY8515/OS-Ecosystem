# OS Ecosystem v0.7.1 Release Notes

Status: Release Ready
Release type: Patch
Publication: Authorized after final validation

## Summary

v0.7.1 changes the presentation layer only. It replaces the v0.7.0 black card-dashboard composition with a concept-as-interface World Atlas while preserving every product boundary, Route, Registry, Contract, Governance responsibility, Capability, AI Hub behavior, and 6W Metadata contract.

## UI changes

- Official product brands remain English: Ultra Brain, OS Ecosystem, Living OS, Universal Learning Engine, and AI Hub.
- User-facing functions, actions, locations, states, and guidance are Korean-first.
- The official hierarchy is `Universe → Ultra Brain → Meta OS → OS Ecosystem → Project → Subsystem → Module → Capability → Engine`.
- OS Ecosystem is the Fruit on the Meta OS branch; its internal World Tree is the current Navigation Hub.
- Living OS, Universal Learning Engine, and AI Hub are exactly three Dome Project Seeds, each containing its own Sapling and ecosystem.
- Subsystem, Module, Capability, Engine, Governance, Registry, and Contract remain inside their responsible Project surfaces or documentation and do not appear on Home.
- A secondary world HUD replaces duplicate top-menu and card navigation without becoming a conventional dashboard header.
- Desktop shows the Fruit interior as one locked, full-world composition.
- 390px Mobile reflows the same world into a Fruit overview, two side Seeds, and a centered AI Hub Seed.
- AI Hub uses the shared Project Seed language while retaining its internal functions inside the same product shell and existing Route.
- A project-owned master key visual establishes the official fruit-interior world, World Tree, and exactly three Project Seeds without image-rendered text.
- The approved composition is treated as a locked UI blueprint; art refinement changes only repetitive foliage, terrain, glass, material, and lighting treatment.
- Home markup contains no Capability, Registry, Contract, Route, or 6W Metadata disclosure; those contracts remain authoritative outside Home.
- Semantic HTML/CSS hit regions follow the visible Seed silhouettes, making each illustrated Seed the actual link rather than a background under a separate control.
- Final Polish aligns Seed boundaries, label spacing, typography, and restrained hover/focus/active feedback without changing card geometry or project placement.
- The selected OS Ecosystem World Tree label opens the repository-owned `?view=overview` integration route in the current tab.
- Excessive glow, decorative animation, meaningless gradients, remote fonts, and dashboard card grids are excluded.

## Preserved contracts

- [Architecture](../architecture/ARCHITECTURE.md)
- [Metadata Contract](../architecture/METADATA_CONTRACT.md)
- [Navigation Contract](../architecture/NAVIGATION_CONTRACT.md)
- [Governance responsibility boundary](../governance/RESPONSIBILITY_BOUNDARY.md)
- [Route Registry](../registry/ROUTE_REGISTRY.md)
- [Contract Registry](../registry/CONTRACT_REGISTRY.md)

Living OS and Universal Learning Engine still open their direct public Streamlit URLs in new tabs. AI Hub remains repository-internal at `?project=ai-hub`.

## Release condition

Desktop 1440×1000, Tablet 820×1180, and Mobile 390×844 renders, internal navigation, direct external endpoints, focus states, console output, and all 201 automated tests passed. The user authorized publication once these Release Ready gates were confirmed.
