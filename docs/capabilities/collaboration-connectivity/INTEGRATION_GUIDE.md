# Integration Guide

Version: v1.0.0

## Register a provider

1. Subclass `BaseConnector` or configure `InMemoryConnector` for tests.
2. Create immutable `ConnectorMetadata` with explicit supported operations, timeout, retry policy, and enabled state.
3. Register it with `ConnectorRegistry`.
4. Construct `CollaborationConnectivityService` with optional Safety and Enhancement gateways.
5. Submit a `ConnectionRequest` and inspect the typed `ConnectionResponse`.

## Safety

The built-in gateway provides deterministic local checks. A deployment can inject a `SafetyGateway` adapter backed by Safety Capability policy. It must validate both request and response and expose a recovery strategy. Denied work never calls the provider.

## Enhancement

Inject an `EnhancementGateway` to consume connection results. `ExecutionRecorder.analytics()` already exposes total execution count, success rate, average response time, connector/operation performance, and repeated errors without storing payloads.

## Automation

Automation calls `service.execute_connector_request(request)`. This is an adapter alias over the governed service path, so automated work cannot skip connector validation, Safety, failure normalization, or recording.

## Import, export, messaging, and sync

Use the dedicated pure functions and managers when no provider execution is required. Business schemas, durable storage, destination authorization, and conflict policy remain the caller's responsibility.
