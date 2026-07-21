# OS Ecosystem

OS Ecosystem is a focused launcher that connects independent projects without exposing their internal capabilities, databases, or runtimes.

**Current version:** v0.2.1
**Status:** Release candidate
**Initial projects:** Living OS, Universal Learning Engine

## Product contract

- No sidebar and no conventional dashboard.
- `OS ECOSYSTEM` remains the visual center.
- Projects appear as surrounding nodes.
- Selecting a connected node opens that project's own UI.
- Each project remains independently owned, versioned, deployed, and operated.
- Capability, database, runtime, and integration details are not presented in the launcher.

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
