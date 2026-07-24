# OS Ecosystem Common UI System

Version: v0.7.1
Status: Official world-design candidate awaiting rendered-screen approval

## Official hierarchy

The common design language follows one fixed hierarchy:

`Universe → Ultra Brain → Meta OS → OS Ecosystem → Project → Subsystem → Module → Capability → Engine`

Each level manages or contains the level directly below it. The UI does not change Repository ownership, Route contracts, runtime boundaries, or Governance authority.

## Concept as interface

Concept art is not a background reference. The explorable world is the interface itself. Every visual object represents a real location, action, state, relationship, or growth stage.

The final official answer-sheet visual is maintained as a project-owned visual asset at
`assets/os-ecosystem-official-answer-v071-final-key-visual.png`. It supplies the Fruit boundary,
World Tree, three Project Seeds, material, lighting, and locked spatial composition.
The final polish changes only art direction: natural materials and foliage, controlled
light and glass response, reduced procedural micro-patterns, stable tonal balance, and a quieter long-viewing palette. The world
structure, composition, object positions, project relationships, and hit-map geometry
remain locked to the official answer.
Semantic HTML links are calibrated to the visible Seed silhouettes so the illustrated
objects themselves are the controls. HTML/CSS supplies only labels, state feedback,
route behavior, and accessibility semantics; it does not introduce a separate card or
panel layer. The artwork contains no interface text.

| World language | Official interface meaning |
| --- | --- |
| Universe | the shared space containing every world |
| Ultra Brain | the greatest World Tree containing the universe |
| Meta OS | a great branch extending from Ultra Brain and managing OS Ecosystems |
| OS Ecosystem | a great fruit on the Meta OS branch; its interior contains another universe |
| OS Ecosystem World Tree | the current product, current location, and Navigation Hub inside the fruit; opens OS Ecosystem Overview |
| Branch | a relationship from the World Tree to a Project Seed |
| Project Seed | Living OS, Universal Learning Engine, or AI Hub; a dome containing its own Sapling and ecosystem |
| Sapling | the growing Project ecosystem visible inside a Project Seed |
| Internal layer | Subsystem, Module, Capability, or Engine inside its responsible Project |
| Foundation | Governance, Registry, Contract, Architecture, and traceability managed outside Home |
| Growth | learning, activation, maturity, and connection expansion |

Decorative objects with no product meaning are prohibited. A Project is represented as a dome Seed containing a Sapling, never as another mature World Tree or a rectangular card. Home contains exactly three Project Seeds and no lower-level function entry.

## Usability priority

A first-time user must identify within three seconds:

1. which object is clickable,
2. where it will go,
3. whether it opens internally or in a new tab,
4. the current location and Home route.

Every Project action uses a clear dome shape, Korean-first function label, route arrow, and visible hover/focus state. The selected current location is explicit. Home has no instructional or descriptive copy. State motion is short and functional; no essential information depends on motion or hover.

## Common components

- `OrientationBar`: a secondary world HUD for product identity, current location, and Home; never a dashboard navigation bar
- `FruitUniverse`: the visible boundary of the OS Ecosystem fruit interior
- `WorldTreeHub`: current location and the central relationship map
- `ProjectSeed`: full-area clickable Project dome containing a Sapling
- `ProjectSeedLabel`: semantic English brand, Korean function label, and route behavior
- `InternalGrowthLayer`: Project-owned Subsystem, Module, Capability, or Engine surface, never a Home entry
- `MobileWorldMap`: Fruit overview followed by a two-seed row and centered AI Hub Seed at 390px
- `MetadataContract`: 6W traceability retained in Architecture and Registry, never emitted on Home
- `FieldZone`: quiet detail area without dashboard cards
- `StatePanel`: shared 준비, 비어 있음, 로딩, 오류 language
- `PrimaryAction`: explicit verb and destination

## State contract

- `Hover`: subtle lift or boundary change that confirms the full hit area
- `Focus`: keyboard-visible outline with information equivalent to Hover
- `Selected`: explicit current-location label and `aria-current`
- `Motion`: restrained transition only; no continuous decorative animation
- `Reduced motion`: all nonessential transitions are removed

## Commercial-quality constraints

- no excessive glow, continuous decorative animation, visual noise, or low-contrast body copy
- the visual target is an AAA game main menu, official concept art, premium fantasy illustration, and brand key visual
- no excessive symmetry, smeared foliage or bark, plastic texture, ornamental gold, or immediately recognizable generated-image mannerisms
- no generated illustration used as an unlabeled or ambiguous interaction layer
- no rectangle-card-centric dashboard or duplicated top navigation
- no image-rendered text; labels and states remain semantic HTML/CSS
- Korean-first titles, actions, lists, status, empty, error, and loading language; official English brands remain unchanged
- local system fonts only; no render-blocking remote font request
- depth comes from authored composition, natural materials, restrained color, hierarchy, spacing, line work, and meaningful silhouettes
- focus-visible, keyboard navigation, reduced motion, and semantic HTML are mandatory
- the visible raster Seed and its semantic link share the same geometry; code adds controllability without creating a separate UI object

## Responsive contract

Desktop presents the fruit interior and complete ecosystem as one large world, not a centered mobile-width layout.

At 390px, the world is reflowed rather than reduced to a tiny desktop image:

`Fruit Interior overview → Living OS Seed + Universal Learning Engine Seed → AI Hub Seed`

The same labels, destinations, and route behavior remain. Touch targets are at least 44px, horizontal page overflow is prohibited, and primary Projects remain within one vertical exploration path.

## Shared adoption

Living OS, Universal Learning Engine, Meta OS, and Ultra Brain may adopt these tokens, silhouettes, state rules, and component semantics. Adoption does not transfer Repository ownership or Governance authority. Each Project develops its own universe and ecosystem while preserving the common hierarchy and action clarity.

## Acceptance contract

- the concept world itself contains the usable navigation
- the World Tree is a real Navigation Hub, not decoration
- Living OS, Universal Learning Engine, and AI Hub are exactly three Project Seeds containing Saplings
- Subsystem, Module, Capability, Engine, Governance, Registry, and Contract do not appear on Home
- every clickable object is a semantic link or button with a visible destination
- every external Project declares “새 탭”
- current location is explicitly selected
- no page-level horizontal overflow at 390px
- no essential information depends on hover, motion, glow, or color alone
