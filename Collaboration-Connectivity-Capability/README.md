# Collaboration & Connectivity Capability

Version: v1.0.0
Status: Stable

This independent OS Ecosystem package defines project-neutral contracts for connector registration, governed request delivery, import/export, basic data transformation, local messaging, synchronization records, health checks, failure handling, and execution evidence.

It does not own project business logic, credentials, user data, a distributed broker, or production provider implementations. Providers are replaceable through `BaseConnector`; Safety, Enhancement, and Automation connect through explicit gateway protocols.

## Run tests

    python -m pytest tests -q

## Public entry points

- `ConnectorRegistry` and `ConnectorMetadata`
- `BaseConnector` and `InMemoryConnector`
- `ConnectionRequest` and `ConnectionResponse`
- `CollaborationConnectivityService`
- `ImportRequest`, `ExportRequest`, and transformation rules
- `InMemoryMessageBus`
- `SynchronizationManager`
- `ExecutionRecorder`

Authoritative architecture, contracts, security, integration, and release documentation is maintained in [docs/capabilities/collaboration-connectivity](../docs/capabilities/collaboration-connectivity/README.md).
