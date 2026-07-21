# OS Ecosystem Structure

Version: v0.4.4

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

Connected projects and capabilities remain independently versioned product surfaces. Moving documentation does not import their internals into the launcher or change runtime behavior.

## Placement rule

Choose the narrowest authoritative category for every new document. Capability documents use docs/capabilities/<capability-name>. Package-local READMEs may contain operational instructions, but they must link to the central documentation index.
