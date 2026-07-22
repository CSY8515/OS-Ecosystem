# OS Ecosystem Structure

Version: v0.6.2

## Repository layout

- .github/workflows: repository validation automation
- .streamlit: launcher theme and deployment configuration example
- app.py: Streamlit launcher entry point
- VERSION: current OS Ecosystem version
- README.md: repository entry and documentation map
- tests: launcher, regression, and documentation-structure tests
- docs: all authoritative ecosystem and capability documentation
- Safety-Capability: independent Safety package and operational README
- Enhancement-Capability: independent Enhancement package and operational README
- Automation-Capability: independent Automation package and operational README
- Collaboration-Connectivity-Capability: independent connection contracts, runtime, and operational README
- Personal-Secretary-Capability: independent advisory package and operational README
- AI-Hub: integrated common AI platform component with `src`, `tests`, `docs`, `config`, and an ignored runtime `data` boundary
- Living-OS: independently owned connected project workspace
- Universal-Learning-Engine: independently owned connected project workspace

## Documentation layout

- docs/architecture: architecture, master design, repository structure, and roadmap
- docs/governance: constitution, rules, principles, standards, policies, decisions, and conventions
- docs/registry: project, capability, version, and release registries
- docs/release: release notes, version history, and migration notes
- docs/capabilities: common capability documentation rule
- docs/capabilities/safety: Safety design, contracts, gates, notes, and history
- docs/capabilities/enhancement: Enhancement design, integration contract, notes, and history
- docs/capabilities/automation: Automation design, integration contract, notes, and history

## Ownership rule

The repository root contains runtime entry points, package boundaries, tests, and navigation files only. All authoritative design and lifecycle documents live under docs.

Living OS and Universal Learning Engine remain independently owned connected project surfaces. Capabilities retain their package boundaries. AI Hub is the explicit exception: it is owned by this repository, imported only through its package boundary, rendered by the OS Ecosystem application, and released under the OS Ecosystem version and tag.

## Placement rule

Choose the narrowest authoritative category for every new document. Capability documents use docs/capabilities/<capability-name>. Package-local READMEs may contain operational instructions, but they must link to the central documentation index.
