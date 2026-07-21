# Messaging Contract

Version: v1.0.0

`CollaborationMessage` contains message ID/type, source, target, payload, priority, creation/expiration time, correlation ID, and metadata. Statuses are `CREATED`, `SENT`, `DELIVERED`, `FAILED`, `EXPIRED`, and `REJECTED`.

The v1.0 `InMemoryMessageBus` is a local validation foundation. It accepts valid non-expired messages, returns destination messages ordered by priority and creation time, and records delivery state. It is not durable, distributed, or suitable as a production broker.

Projects own message semantics, consumer authorization, idempotency rules, and payload retention. Production providers must implement the [Connector Contract](./CONNECTOR_CONTRACT.md) and preserve the same message envelope and failure semantics.
