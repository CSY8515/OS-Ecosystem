# OS Ecosystem v0.2.0 Release Notes

Status: Release candidate

## Included

- A dedicated Streamlit launcher with no sidebar or conventional dashboard.
- Central `OS ECOSYSTEM` identity with surrounding project nodes.
- Living OS as a connected production destination.
- Universal Learning Engine as a configuration-ready destination.
- Safe HTTP(S) destination validation and a clear pending state.
- Responsive mobile layout and reduced-motion support.
- Architecture, structure, roadmap, master design, and deployment guidance.
- Automated launcher contract tests.

## Product boundaries

- Connected projects remain independently owned, versioned, tested, and deployed.
- The launcher does not import, execute, or persist project internals.
- Capability, database, runtime, secret, and health details remain outside the user interface.
- Safety Capability remains an internal repository component and is not a launcher node.

## Release identity

- Repository: OS Ecosystem
- Version and intended tag: `v0.2.0`
- Living OS baseline: `v2.0.4`
- Universal Learning Engine baseline: `v1.0.0`

## Publication gates

- Automated tests must pass.
- A Streamlit smoke test must reach a healthy state.
- `ULE_URL` must be configured after the Universal Learning Engine has a production deployment.
- GitHub release and Streamlit deployment remain pending until publication credentials are available.
