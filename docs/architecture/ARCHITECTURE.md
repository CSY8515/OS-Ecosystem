# OS Ecosystem Architecture

Version: v0.7.0

## Purpose

OS Ecosystem is the integrated operating layer that provides shared Navigation, Capability, AI operations, Governance, and Registry while retaining independent System ownership and deployment boundaries.

## Official hierarchy

```text
OS Ecosystem (OS System)
|-- OS Ecosystem Core
|   |-- Safety Capability v1.0.0
|   |-- Enhancement Capability v1.0.0
|   |-- Automation Capability v1.0.0
|   |-- Collaboration & Connectivity Capability v1.0.0
|   `-- Personal Secretary Capability v1.0.0
|-- AI Hub v0.1.0 (repository-internal component)
|-- Living OS v2.0.4 (independent connected system)
`-- Universal Learning Engine v1.0.0 (independent connected system)
```

각 계층은 직접 하위 계약만 관리합니다. Each layer manages only its direct child contracts. OS Ecosystem does not own the internal UI, data, Runtime, or Release of Living OS or Universal Learning Engine.

## Product shell and UI system

Home and AI Hub share the Header, Navigation, Breadcrumb, action, state, and responsive rules in the [Navigation Contract](./NAVIGATION_CONTRACT.md). The explorable world follows the [Common UI System](./UI_SYSTEM.md): OS Ecosystem is the Fruit on the Meta OS branch, its internal World Tree is Core and Navigation Hub, and each Project is a Dome Seed containing its own Sapling and ecosystem. The Home world exposes only Living OS, Universal Learning Engine, and AI Hub; Subsystem, Module, Capability, Engine, Governance, Registry, and Contract remain inside their responsible Project surfaces or documentation. Concept reuse by other Systems does not change ownership or Governance.

User explanations and Registry entries use the [6W Metadata Contract](./METADATA_CONTRACT.md).

## Runtime flow

1. Streamlit loads the common product shell and public Registry.
2. External destinations resolve from Secrets, environment variables, or approved defaults and only HTTP(S) is accepted.
3. Living OS and Universal Learning Engine open through direct full-card links with `target="_blank"` and `noopener noreferrer`.
4. AI Hub renders at the internal `?project=ai-hub` route.
5. Capabilities are invoked only through public contracts and do not own project data.

## Capability flow

- Automation: `Validation → Risk Check → Approval → Execution → Logging`, with Recovery after failure
- Connectivity: `Request → Safety validation → Provider execution → Response validation → Sanitized record`
- Personal Secretary: `Project snapshots → deterministic synthesis → Safety validation → recommendation → user decision`
- AI Hub: provider-neutral settings, routing, status, and usage contracts; no credentials or raw sensitive data in UI

## Public and hidden boundaries

Public information includes System and Capability identity, purpose, version, status, Route, 6W explanation, and approved Contract. Databases, schemas, processes, credentials, secrets, internal adapters, and raw health data remain hidden.

## Governance boundary

OS Ecosystem owns connection, Registry, compatibility, validation, AI Hub lifecycle, and Release. It does not interpret or replace Ultra Brain-only Governance. The authority is defined by the [Responsibility Boundary](../governance/RESPONSIBILITY_BOUNDARY.md).

## Deployment

OS Ecosystem Core and AI Hub deploy as one Streamlit application. Living OS and Universal Learning Engine retain independent deployments.
