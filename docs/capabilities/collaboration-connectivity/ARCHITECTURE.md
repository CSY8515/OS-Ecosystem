# Collaboration & Connectivity Architecture

Version: v1.0.0

## Structure

```text
Project / Automation
        |
ConnectionRequest
        |
SafetyGateway validation
        |
CollaborationConnectivityService
        |
ConnectorRegistry -> BaseConnector -> Provider adapter
        |
ConnectionResponse
        |
ExecutionRecorder -> Enhancement analytics input
```

Import/export, transformation, messaging, synchronization, and health are neighboring public modules. They share stable models and enums but remain independently testable.

## Ownership

The capability owns envelopes, provider registration, state classification, basic format conversion, delivery state, retry decisions, and sanitized execution evidence. A source project owns payload meaning, schema authority, conflict policy, authorization policy, and persistence.

## Extension model

Providers subclass `BaseConnector`, publish immutable `ConnectorMetadata`, explicitly list supported operations, and register with `ConnectorRegistry`. Unsupported operations always return the standard `UNSUPPORTED_OPERATION` failure through the service. Provider replacement requires no consumer contract change.

## Cross-capability integration

- Safety validates request identity, connector state, operation permission, payload size, risk, and response identity before results cross the boundary.
- Enhancement receives sanitized response and aggregate execution data for success-rate, latency, failure-pattern, provider-stability, and sync analysis.
- Automation invokes the same `ConnectionRequest` through `execute_connector_request`; it receives a normal `ConnectionResponse` and cannot bypass Safety.

See the [Master Design](./MASTER_DESIGN.md) for invariants and the [Integration Guide](./INTEGRATION_GUIDE.md) for usage.
