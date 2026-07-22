# AI Hub v0.1 API Contract

Status: Implemented candidate

The public application operation is `InferenceService.execute`. Transport adapters must preserve the following provider-neutral fields.

## Request

- `request_id`: caller-scoped idempotency identity
- `caller_id`: registered OS Ecosystem project
- `task_kind`: generation, reasoning, summarization, extraction, classification, or structured_generation
- `messages`: system/developer/user/assistant text messages
- `max_output_tokens`: positive caller request bounded by model registration
- `response_format`: text or JSON

## Response

- correlation and request IDs
- success and normalized output
- selected provider/model IDs
- total duration and attempt count
- routing policy version
- normalized usage when known
- failover indicator
- stable error code and retryability on failure

Provider SDK objects, credentials, stack traces, raw provider errors, and internal records never cross this boundary. Caller authorization requires the `inference` scope. Current idempotency is runtime-local; durable cross-restart idempotency is not claimed.
