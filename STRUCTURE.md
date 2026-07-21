# OS Ecosystem Structure

Version: v0.3.3

```text
OS-Ecosystem/
|-- .streamlit/
|   |-- config.toml                 # launcher theme and navigation settings
|   `-- secrets.toml.example        # destination configuration example
|-- Living-OS/                      # independent connected project
|-- Universal-Learning-Engine/      # independent connected project
|-- Safety-Capability/              # independent safety capability; surfaced in Capability UI
|-- Enhancement-Capability/         # independent shared learning and optimization capability
|-- tests/
|   `-- test_launcher.py            # launcher contract tests
|-- app.py                          # Streamlit launcher entry point
|-- VERSION                         # current OS Ecosystem version
|-- ARCHITECTURE.md
|-- MASTER_DESIGN.md
|-- ROADMAP.md
|-- RELEASE_NOTES.md
|-- README.md
`-- requirements.txt
```

## Ownership rule

Root files define only OS Ecosystem. Connected project directories remain independent product surfaces. Their internal modules, data, and runtime are not imported by the root launcher.
