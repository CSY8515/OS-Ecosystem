# Governance Decisions

## DEC-0001: Central documentation root

Status: Accepted
Current release: v0.7.0

## ADR: Collaboration & Connectivity as an independent capability

Decision: use provider-neutral request, response, connector, messaging, synchronization, and execution contracts. Preserve project data ownership and require explicit Safety validation. Ship only in-memory demonstration providers in v1.0.0.

All authoritative architecture, governance, registry, release, and Capability documents are managed under docs/. Root and Capability READMEs remain operational entry points. CI validates required paths and internal links. Runtime contracts remain unchanged.
