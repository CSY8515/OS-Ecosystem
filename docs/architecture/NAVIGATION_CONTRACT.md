# OS Ecosystem Navigation Contract

Version: v0.7.0

## Product shell

Every OS Ecosystem surface uses one product shell:

- Header: product identity, current version, and operating status
- Navigation: Home, Projects, AI Hub, Capabilities, Governance, Architecture, Registry
- Breadcrumb: current position and a clear route back to Home
- Page title: Korean-first title with an optional official English label
- State language: Korean-first 준비, 비어 있음, 로딩, 오류, 이용 불가 patterns with one shared visual frame
- World Explorer: concept-as-interface navigation defined by the [Common UI System](./UI_SYSTEM.md)

## Route rules

- Home and documentation sections use stable in-page anchors.
- AI Hub uses the repository-owned internal route `?project=ai-hub`.
- Living OS and Universal Learning Engine use direct public HTTPS URLs in a new tab.
- Internal routes never open a new tab.
- External routes use `target="_blank"` and `rel="noopener noreferrer"`.

## Interaction rules

Clickable nodes and cards have a visible action verb, arrow, stronger border, destination type, focus state, and full-card hit area. Informational landmarks use a quieter border, have no `href`, and state “현재 위치” or their information role. The Interaction Guide explains these rules before the user reaches the world map.

Mobile and desktop preserve the same labels, action order, destination semantics, and action-versus-landmark distinction. In the narrow linear layout, Action Nodes precede the informational Core landmark so a clickable destination remains visible in the initial viewport; only the compact Navigation row may scroll horizontally.
