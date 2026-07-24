# OS Ecosystem Master Design

Canonical version: v0.7.0

## Product definition

OS Ecosystem is an explorable operating world, not a launcher list or decorative concept image. Independent Systems, internal components, Capabilities, Governance, and Registry appear in one coherent product language without changing their ownership boundaries.

## Official visual direction

The concept art is the interface:

- Universe is the shared space containing every world,
- Ultra Brain is the greatest World Tree,
- Meta OS is a great branch extending from Ultra Brain,
- OS Ecosystem is a great Fruit on the Meta OS branch,
- the World Tree inside that Fruit is OS Ecosystem Core and the Navigation Hub,
- Living OS, Universal Learning Engine, and AI Hub are exactly three Dome Project Seeds,
- each Project Seed contains its own growing Sapling and ecosystem,
- Subsystem, Module, Capability, Engine, Governance, Registry, Contract, and Architecture remain inside their responsible Project surface or documentation rather than appearing on Home.

The authoritative component and usability rules are in the [Common UI System](./UI_SYSTEM.md).

## Experience priority

1. Usability is more important than world-building.
2. A new user must recognize action, destination, and tab behavior within three seconds.
3. Action objects use intentional silhouettes, arrows, explicit verbs, and full-object hit areas.
4. Current location and information landmarks do not imitate buttons.
5. Korean comes first; official English identity is secondary.
6. Header, Navigation, Breadcrumb, button, card, and state language stay consistent.
7. Empty, Error, Loading, Ready, and Unavailable states explain the next step.
8. Database, Runtime, Credential, and internal implementation remain hidden.

## Art direction restraint

The commercial product should look like an official visual commissioned from a
professional art team. The quality bar is an AAA game main menu, official
concept art, premium fantasy illustration, and a long-lived brand key visual.
Excessive glow, decorative animation, meaningless effects, excessive symmetry,
smeared foliage, plastic materials, ornamental gold, visual noise, and
unreadable contrast are prohibited.

The project-owned master artwork at
`assets/os-ecosystem-official-answer-v071-final-key-visual.png` expresses the OS Ecosystem
fruit interior, World Tree, and exactly three Project Seeds. It contains no interface text. Semantic
HTML/CSS overlays own all labels, destinations, hit areas, Hover, Focus,
Selected, responsive behavior, and accessibility. The art is therefore part of
the interface without becoming a background-only decoration or an ambiguous
image map.

## Screen structure

- sidebar-free common Product Header
- Korean-first Navigation and Breadcrumb
- Fruit-interior World Atlas containing the three real Project routes
- Dome Project Seeds for Living OS, Universal Learning Engine, and AI Hub
- a growing Sapling visible inside every Project Seed
- no explanatory copy or internal Architecture terms on Home
- AI Hub detail surface on its existing internal route
- the same world and Seed semantics reflowed for mobile

## Route behavior

Living OS and Universal Learning Engine are Project Seeds opening their real HTTPS applications in new tabs. AI Hub is a Project Seed opening the internal route. OS Ecosystem Core is the selected World Tree Navigation Hub. Capability and lower-level functions retain their contracts but do not appear on Home.

## Acceptance criteria

- the concept world itself is usable navigation
- every Project Seed exposes its brand and destination behavior before click
- external links use direct URLs, new tabs, and safe rel attributes
- no redirect mechanisms are implemented
- Home and AI Hub share the same shell and design tokens
- 390px mobile has no horizontal overflow
- keyboard focus and reduced motion are supported
- existing Capability and AI Hub behavior remains compatible
