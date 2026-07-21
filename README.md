# OS Ecosystem

OS Ecosystem is the governance, architecture, registry, and navigation layer that connects independent projects without merging their runtimes.

**Current version:** v0.2.3
**Status:** Stable
**Initial projects:** Living OS, Universal Learning Engine
**Production:** https://8javbq85jtappi6tkdhkt7g.streamlit.app/

## Product contract

- No sidebar and no conventional dashboard.
- A compact menu exposes Projects, Governance, Architecture, and Registry without adding a sidebar.
- `OS ECOSYSTEM` remains the visual center.
- Projects appear as surrounding nodes.
- Selecting a connected node opens that project's own UI.
- Each project remains independently owned, versioned, deployed, and operated.
- Governance, architecture, and registry identifiers are visible while databases, runtimes, credentials, and operational internals remain hidden.

## Run locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

Production URLs for Living OS and Universal Learning Engine are included as defaults. Both destinations can be overridden with `LIVING_OS_URL` and `ULE_URL` in Streamlit Secrets or the environment.

## Documentation

1. [VERSION](./VERSION) - current release identity
2. [ARCHITECTURE.md](./ARCHITECTURE.md) - boundaries and runtime flow
3. [STRUCTURE.md](./STRUCTURE.md) - repository layout
4. [ROADMAP.md](./ROADMAP.md) - delivery sequence and future scope
5. [MASTER_DESIGN.md](./MASTER_DESIGN.md) - canonical product and visual design
6. [RELEASE_NOTES.md](./RELEASE_NOTES.md) - release evidence
