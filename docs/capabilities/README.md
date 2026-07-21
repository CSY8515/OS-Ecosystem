# Capability Documentation Standard

Version: v0.5.0

Every Capability uses docs/capabilities/<capability>/ as its authoritative documentation root.

Required files are README.md, ARCHITECTURE.md, INTEGRATION_CONTRACT.md, RELEASE_NOTES.md, and CHANGELOG.md. Additional contracts are allowed where needed.

Capability code remains in <Name>-Capability/. Its README is an operational entry point. New Capabilities must be added to the [Capability Registry](../registry/CAPABILITY_REGISTRY.md), and every internal link must pass validation.
