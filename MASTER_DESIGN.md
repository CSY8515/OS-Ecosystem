# OS Ecosystem Master Design

Canonical version: v0.2.2

## Product statement

OS Ecosystem is the quiet front door to a family of independent systems. It creates coherence through navigation, not by merging products or exposing their machinery.

## Experience principles

1. **Center before chrome.** The first visual anchor is `OS ECOSYSTEM`, not navigation furniture.
2. **Projects, not internals.** Users choose outcomes and project identities; capabilities, databases, and runtimes remain hidden.
3. **One deliberate action.** A project node opens that project's UI directly.
4. **Independent by design.** Connection never implies shared data ownership or a shared release lifecycle.
5. **Calm technical confidence.** The interface feels precise, spacious, and operational without becoming a monitoring dashboard.

## Spatial design

- Full-viewport canvas with no sidebar.
- Circular central core containing the ecosystem identity and version.
- Connected project nodes placed on opposing sides of the core.
- Thin connection lines communicate membership, not data flow.
- On narrow screens, the core and nodes form a clear vertical sequence.

## Visual language

- Near-black green background with a restrained grid.
- Soft cyan as the single system accent.
- Neutral sans-serif typography with compact technical labels.
- Subtle orbital lines and ambient light; no decorative imagery.
- Reduced-motion preferences disable rotation and transitions.

## Node states

- **Connected:** full contrast, interactive, and opens the project UI.
- **Pending:** muted, non-interactive, and clearly requests a deployment address.
- Internal errors and operational details are never exposed as node content.

## Initial node copy

### Living OS

“삶의 기록과 운영을 하나의 흐름으로”

### Universal Learning Engine

“어떤 주제든 구조화된 학습 경험으로”

## Acceptance criteria

- No visible Streamlit sidebar, toolbar, or generic dashboard cards.
- `OS ECOSYSTEM` is centered at desktop widths.
- Living OS and Universal Learning Engine are the only public project nodes.
- Connected nodes navigate to configured HTTP(S) project UIs.
- Missing or invalid destinations cannot become unsafe links.
- Layout remains usable on mobile and with reduced motion.
- No internal Capability, DB, Runtime, or credential details appear in the rendered UI.
