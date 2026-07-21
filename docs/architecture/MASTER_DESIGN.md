# OS Ecosystem Master Design

Canonical version: v0.5.0

## Product statement

OS Ecosystem is the quiet governance and navigation layer for a family of independent systems. It creates coherence through shared rules, architecture, registries, and direct project entry without merging runtimes.

## Experience principles

1. **Center before chrome.** The first visual anchor is `OS ECOSYSTEM`, not navigation furniture.
2. **Governed visibility.** Users can inspect approved governance, architecture, and registry identities while implementation details remain hidden.
3. **One deliberate action.** A project node opens that project's UI directly.
4. **Independent by design.** Connection never implies shared data ownership or a shared release lifecycle.
5. **Calm technical confidence.** The interface feels precise, spacious, and operational without becoming a monitoring dashboard.

## Spatial design

- Full-viewport canvas with no sidebar.
- Compact top navigation for Projects, Capability, Automation, Connectivity, Governance, Architecture, and Registry.
- Document-like ecosystem sections continue below the preserved central launcher.
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
- Governance contains Constitution, Rules, Principles, Standards, and Policies.
- Architecture contains Master Architecture, Repository Strategy, Integration Strategy, and Roadmap.
- Registry contains Project Registry, Capability Registry, and Release History.
- Capability contains Safety, Enhancement, Automation, and Collaboration & Connectivity, with each Capability's approved core modules visible.
- Automation has a dedicated overview showing Workflow, Scheduler, Trigger, Routine, Auto Execution, and Auto Decision.
- The governed automation flow is visible as Validation, Risk Check, Approval, Execution, Logging, and Recovery.
- Collaboration & Connectivity displays capability version, registered/available/degraded connectors, last health check, and recent result with demo state clearly labeled.
- Connected nodes navigate to configured HTTP(S) project UIs.
- Missing or invalid destinations cannot become unsafe links.
- Layout remains usable on mobile and with reduced motion.
- Capability registry identity may be shown, but databases, runtimes, credentials, and implementation details remain hidden.

## Documentation management

All authoritative design, governance, registry, release, and capability documents are managed under docs. Documentation placement and links are part of the repository contract; documentation-only patches must preserve the runtime and visual product contract.
