# OS Ecosystem Common UI System

Version: v0.7.0
Status: Official direction

## Concept as interface

Concept art is not a background reference. The explorable world is the interface itself. Every visual object must represent a real location, action, state, relationship, or growth stage.

| World language | Interface meaning |
| --- | --- |
| Space | the shared operating environment and available exploration area |
| World Tree | the current OS Core and stable navigation landmark |
| Branch | an explicit route or ownership relationship |
| Fruit | an independently operating connected System |
| Seed | an internal or newly growing System |
| Growth | Capability activation, learning, or maturity |
| Root | Governance, Registry, Contract, and traceability foundation |

Decorative objects with no product meaning are prohibited.

## Usability priority

A first-time user must identify within three seconds:

1. which object is clickable,
2. where it will go,
3. whether it opens internally or in a new tab.

Every action therefore uses a stronger border, an explicit “클릭하여 이동” or equivalent verb, an arrow, a destination label, and a visible focus state. Landmarks and information use a quieter border and never imitate a button.

## Common components

- `ProductHeader`: product identity, version, current navigation state
- `Breadcrumb`: current location and Home route
- `WorldExplorer`: concept world containing real navigation
- `WorldActionNode`: full-card clickable System, Fruit, Seed, or Capability
- `WorldLandmark`: current position or non-clickable information
- `InteractionGuide`: concise action/landmark/route legend
- `GrowthAxis`: Seed → Capability → Fruit meaning
- `MetadataDisclosure`: optional 6W context without cluttering primary actions
- `StatePanel`: shared 준비, 비어 있음, 로딩, 오류, 이용 불가 language with Korean as the primary visible label
- `PrimaryAction`: explicit verb and destination

## Commercial-quality constraints

- no excessive glow, continuous decorative animation, visual noise, or low-contrast body copy
- no generated illustration used as an unlabeled interaction layer
- user-facing titles, actions, lists, status, empty, error, and loading language are Korean-first; official English identifiers remain secondary
- the product shell uses a local system-font stack and does not require a render-blocking remote font request
- visual depth comes from hierarchy, spacing, borders, and restrained color
- focus-visible, keyboard navigation, reduced motion, and semantic HTML are mandatory
- mobile retains the same action order, labels, and destination semantics; Action Nodes appear before the informational Core landmark in the narrow linear layout
- concept symbols remain code-native SVG/CSS so labels, states, and accessibility stay controllable

## Shared adoption

Living OS, Universal Learning Engine, and Ultra Brain may adopt the same tokens, component semantics, interaction labels, and world mapping. Adoption does not transfer Repository ownership or Governance authority. Each System maps its own domain objects while preserving the action-versus-landmark distinction and destination clarity.

## Acceptance contract

- the concept world itself contains the usable navigation
- every clickable node is a semantic link or button with a verb
- every external node declares “새 탭”
- current location is explicitly labeled and non-clickable
- world symbols have documented product meaning
- no page-level horizontal overflow at 390px; the compact Navigation row alone may scroll horizontally
- at least one clearly labeled Action Node is visible in the initial 390px viewport
- no essential information depends on hover, animation, or glow
