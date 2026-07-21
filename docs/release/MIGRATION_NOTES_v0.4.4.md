# v0.4.4 Documentation Migration Notes

This patch changes documentation locations only.

| Previous | v0.4.4 |
| --- | --- |
| ARCHITECTURE.md | docs/architecture/ARCHITECTURE.md |
| MASTER_DESIGN.md | docs/architecture/MASTER_DESIGN.md |
| ROADMAP.md | docs/architecture/ROADMAP.md |
| STRUCTURE.md | docs/architecture/STRUCTURE.md |
| RELEASE_NOTES.md | docs/release/RELEASE_NOTES_v0.4.4.md |

Capability docs moved from each Capability docs/ directory to docs/capabilities/<capability>/. Capability changelogs and release notes moved with them. Capability READMEs remain beside code as entry points.

No package, API, database, environment, or deployment migration is required.
