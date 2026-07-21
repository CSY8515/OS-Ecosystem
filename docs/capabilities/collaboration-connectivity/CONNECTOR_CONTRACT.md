# Connector Contract

Version: v1.0.0

## Metadata

Every connector declares `connector_id`, `name`, `connector_type`, `provider`, `version`, `status`, `supported_operations`, `authentication_type`, `endpoint_type`, `timeout_seconds`, `retry_policy`, `enabled`, and provider-neutral metadata.

Connector types are `INTERNAL_OS`, `EXTERNAL_API`, `FILE_IMPORT`, `FILE_EXPORT`, `DATABASE`, `WEBHOOK`, `AI_PROVIDER`, `MESSAGE`, and `CUSTOM`. Statuses are `REGISTERED`, `AVAILABLE`, `DEGRADED`, `UNAVAILABLE`, `DISABLED`, and `ERROR`.

## Operations

The base contract defines `connect`, `disconnect`, `health_check`, `send`, `receive`, `import_data`, `export_data`, and `get_status`. A connector lists only supported operations. Calling another operation yields `UNSUPPORTED_OPERATION`.

## Request

`ConnectionRequest` contains request and correlation IDs, connector ID, operation, source, target, payload, headers, metadata, timeout, and creation time.

## Response

`ConnectionResponse` contains request and connector IDs, success, status, data, error code/message, elapsed milliseconds, retryable state, timestamp, and metadata.

## Provider obligations

- Do not hardcode credentials.
- Do not log headers or whole payloads.
- Convert provider failures into typed capability errors when possible.
- Respect timeout and bounded retry policy.
- Return provider-neutral values.
- Implement a deterministic health check or inherit `UNKNOWN`.
