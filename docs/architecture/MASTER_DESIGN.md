# OS Ecosystem Master Design

Canonical version: v0.7.0

## Product definition

OS Ecosystem is an explorable operating world, not a launcher list or decorative concept image. Independent Systems, internal components, Capabilities, Governance, and Registry appear in one coherent product language without changing their ownership boundaries.

## Official visual direction

The concept art is the interface:

- space is the operating environment,
- the World Tree is OS Ecosystem Core,
- branches are explicit routes and relationships,
- fruit represents independent connected Systems,
- seed represents internal growth such as AI Hub,
- growth represents Capability maturity,
- roots represent Governance, Registry, Contract, and traceability.

The authoritative component and usability rules are in the [Common UI System](./UI_SYSTEM.md).

## Experience priority

1. Usability is more important than world-building.
2. A new user must recognize action, destination, and tab behavior within three seconds.
3. Action nodes use strong borders, arrows, explicit verbs, and full-card click areas.
4. Current location and information landmarks do not imitate buttons.
5. Korean comes first; official English identity is secondary.
6. Header, Navigation, Breadcrumb, button, card, and state language stay consistent.
7. Empty, Error, Loading, Ready, and Unavailable states explain the next step.
8. Database, Runtime, Credential, and internal implementation remain hidden.

## Art direction restraint

The commercial product should not look AI-generated. Excessive glow, decorative animation, meaningless effects, visual noise, and unreadable contrast are prohibited. Code-native SVG and CSS express the world because their meaning, state, accessibility, and responsive layout remain controllable.

## Screen structure

- sidebar-free common Product Header
- Korean-first Navigation and Breadcrumb
- concise Interaction Guide
- interactive World Explorer containing the real System routes
- expandable 6W context below primary actions
- Capability growth cards
- AI Hub, Governance, Architecture, and Registry detail sections
- same information order on mobile and desktop

## Route behavior

Living OS and Universal Learning Engine are Fruit action nodes opening their real HTTPS applications in new tabs. AI Hub is a Seed action node opening the internal route. OS Ecosystem Core is the World Tree landmark and explicitly states that it is the current location.

## Acceptance criteria

- the concept world itself is usable navigation
- every action exposes its destination behavior before click
- external links use direct URLs, new tabs, and safe rel attributes
- no redirect mechanisms are implemented
- Home and AI Hub share the same shell and design tokens
- 390px mobile has no horizontal overflow
- keyboard focus and reduced motion are supported
- existing Capability and AI Hub behavior remains compatible
