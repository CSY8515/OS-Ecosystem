# Ecosystem Standards

Version: v0.7.0

- docs/architecture/: system design and repository structure
- docs/governance/: authority and management rules
- docs/registry/: project, Capability, version, and release records
- docs/release/: notes, history, and migrations
- docs/capabilities/: common and per-Capability documents

Directories use lowercase. Authoritative filenames use uppercase snake case. Every release validates paths, links, versions, Streamlit startup, and runtime tests.

Repository-owned platform components may preserve approved product directory names such as `AI-Hub/`. They must keep source, tests, configuration examples, runtime data, and secrets in their documented boundaries and participate in the root CI and release workflow.
