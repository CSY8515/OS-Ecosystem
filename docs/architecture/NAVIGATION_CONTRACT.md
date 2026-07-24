# OS Ecosystem Navigation Contract

Version: v0.72

## Product shell

Every OS Ecosystem surface uses one orientation system:

- Orientation Bar: English brand, Korean-first current location, version state, and Home route
- Cosmic Lineage: `Universe → Ultra Brain → Meta OS → OS Ecosystem`
- World Tree Hub: the current product and central navigation relationship map
- Project Seeds: Living OS, Universal Learning Engine, and AI Hub; every Seed contains its Project Sapling
- Internal layers: Subsystem, Module, Capability, Engine, Governance, Architecture, Registry, and Contract stay off Home
- State language: Korean-first 준비, 비어 있음, 로딩, 오류, 이용 불가 patterns
- World Atlas: concept-as-interface navigation defined by the [Common UI System](./UI_SYSTEM.md)

This orientation system replaces duplicate top-menu and card-grid navigation. It does not replace or rename any Route.

## Route rules

- Home and documentation sections use stable in-page anchors.
- OS Ecosystem Overview uses the repository-owned internal route `?view=overview`.
- AI Hub uses the repository-owned internal route `?project=ai-hub`.
- Living OS and Universal Learning Engine use direct public HTTPS URLs in a new tab.
- Internal routes never open a new tab.
- External routes use `target="_blank"` and `rel="noopener noreferrer"`.
- Redirect intermediaries, login routes, `st.switch_page`, query redirects, and meta refresh remain prohibited.

## Object-to-route mapping

| Interface object | Meaning | Route behavior |
| --- | --- | --- |
| Orientation Home | return to OS Ecosystem | `./`, current tab |
| OS Ecosystem World Tree | current location and Navigation Hub | `?view=overview`, current tab |
| Living OS Project Seed | independent Project containing a Sapling | direct public URL, new tab |
| Universal Learning Engine Project Seed | independent Project containing a Sapling | direct public URL, new tab |
| AI Hub Project Seed | repository-owned Project containing a Sapling | `?project=ai-hub`, current tab |

## Interaction rules

Clickable Project Seeds have a visible Korean function label, route arrow, distinct dome silhouette, Hover/Focus/Active state, and full-object hit area. Hover and Focus slightly lift and brighten the same Seed, strengthen its Project-color boundary, sharpen both label lines, and emphasize the route arrow without Glow, Neon, or Bloom. Active briefly compresses the Seed and returns immediately without delaying navigation. The selected OS Ecosystem World Tree label opens the internal Overview while preserving its current-location meaning. Home uses no instructional or descriptive paragraph.

The selected World Tree uses `aria-current="location"`. External Project Seeds state “새 탭에서 열기”; the internal AI Hub Seed states “현재 화면에서 열기”.

Desktop and Mobile preserve identical destination semantics. At 390px, the world reflows into `Fruit Interior overview → Living OS Seed → Universal Learning Engine Seed → AI Hub Seed`; it is never reduced to an unreadable miniature.
