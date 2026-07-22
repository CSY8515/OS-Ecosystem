# OS Ecosystem

OS Ecosystem is the governance, architecture, registry, capability, and navigation layer that connects independent projects without merging their runtimes.

**Current version:** v0.6.1
**Release type:** Official Project Integration Patch
**Status:** Stable
**Projects:** Living OS, Universal Learning Engine, AI Hub
**Capabilities:** Safety, Enhancement, Automation, Collaboration & Connectivity, Personal Secretary
**Production:** https://8javbq85jtappi6tkdhkt7g.streamlit.app/

## Product contract

- No sidebar and no conventional dashboard.
- A compact menu exposes Projects, AI Hub, Capability, Personal Secretary, Automation, Connectivity, Governance, Architecture, and Registry.
- OS ECOSYSTEM remains the visual center, with independent projects presented as surrounding nodes.
- Project nodes open each project's public Streamlit UI in a new browser tab.
- Governance, architecture, and registry identities are visible while databases, runtimes, credentials, and operational internals remain hidden.
- Living OS, Universal Learning Engine, AI Hub, Safety, Enhancement, Automation, Collaboration & Connectivity, and Personal Secretary keep independent ownership and release boundaries.

## Run locally

    pip install -r requirements.txt
    streamlit run app.py

Living OS and Universal Learning Engine production URLs are configured as direct public destinations. They may be overridden with LIVING_OS_URL and ULE_URL through Streamlit Secrets or the environment. AI Hub uses its in-launcher entry screen until a safe HTTP(S) dashboard destination is supplied through AI_HUB_URL.

## Documentation

All authoritative design and lifecycle documents are managed below [docs](./docs/README.md).

- [Architecture](./docs/architecture/ARCHITECTURE.md): architecture, master design, structure, and roadmap
- [Governance](./docs/governance/CONSTITUTION.md): constitution, rules, principles, standards, policies, decisions, and conventions
- [Registry](./docs/registry/PROJECT_REGISTRY.md): projects, capabilities, versions, and releases
- [Release](./docs/release/RELEASE_NOTES_v0.6.1.md): release notes, version history, and migration notes
- [Capabilities](./docs/capabilities/README.md): the common documentation rule and capability-specific contracts
- [VERSION](./VERSION): current repository release identity

## Repository structure

- app.py and requirements.txt define the Streamlit launcher runtime.
- tests contains ecosystem and documentation contract checks.
- docs contains every authoritative design, governance, registry, release, and capability document.
- Safety-Capability, Enhancement-Capability, Automation-Capability, Collaboration-Connectivity-Capability, and Personal-Secretary-Capability contain independent capability code and local operational READMEs.
- Living-OS and Universal-Learning-Engine remain independent connected project workspaces and are not imported by the launcher.

See the complete [repository structure](./docs/architecture/STRUCTURE.md).

## Documentation management principles

1. New authoritative documents are created in the matching docs category.
2. Capability documentation follows the same central structure as ecosystem documentation.
3. Operational package READMEs may remain beside code but link to their authoritative docs location.
4. Moves must preserve or update every internal Markdown link.
5. Documentation-only patches do not change launcher or capability behavior.
