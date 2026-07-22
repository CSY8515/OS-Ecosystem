# AI Hub v0.1 Master Design

Status: v0.1 Final
Approval: Approved on 2026-07-22
Implementation: Complete; included in OS Ecosystem v0.6.2
Authority: This document defines the proposed v0.1 product boundary. Architecture and repository placement are defined by `ARCHITECTURE.md` and `STRUCTURE.md`.

## 1. Product statement

AI Hub is the shared AI operations platform for OS Ecosystem. Living OS, Universal Learning Engine, and approved future projects send provider-neutral AI requests to AI Hub. AI Hub validates each request, chooses an eligible provider and model, executes it, applies controlled retry or failover, and returns a normalized response with operational metadata.

The primary product is machine-to-machine AI operations. The human-facing interface is an administrative control plane, not an AI chat application.

## 2. Goals

1. Give every approved OS Ecosystem project one stable AI access contract.
2. Prevent callers from depending on a provider SDK, credential, response shape, or model name.
3. Select the best currently eligible provider using explicit, inspectable policy.
4. Continue service through bounded retry and failover when policy permits.
5. Centralize provider health, usage evidence, limits, prediction, and execution records.
6. Keep credentials and sensitive request content out of dashboards and ordinary logs.
7. Add providers without changing the public request and response contract.

## 3. Non-goals for v0.1

- A consumer chat application or conversation-history product
- Autonomous purchasing, quota upgrades, or billing actions
- Automatic provider or model registration from the internet
- Training, fine-tuning, embeddings, image, audio, video, or realtime workloads
- Provider-specific tools, agents, file stores, or proprietary features in the public contract
- Cross-project memory, prompt sharing, or business-data ownership
- AI-driven routing policy changes
- Unbounded retry, background job orchestration, or distributed workflow execution
- Guaranteed semantic equivalence between different providers

## 4. Product principles

1. **Automatic by default.** Callers describe the task and constraints; they do not select a provider in normal operation.
2. **Provider neutral above the adapter boundary.** Provider SDK types never escape an adapter.
3. **Policy before execution.** Validation, eligibility, routing, and security checks precede every provider call.
4. **Explicit authority.** AI Hub may choose and execute AI inference; it may not mutate caller-owned records or make business decisions for the caller.
5. **Bounded failure handling.** Timeouts, retries, and failovers have configured limits and one final outcome.
6. **Evidence, not illusion.** Health, usage, and predictions display timestamps, sources, confidence, and unknown states.
7. **Privacy by default.** Raw prompts and responses are transient unless a separately approved diagnostic policy explicitly retains them.
8. **Integrated lifecycle.** AI Hub owns its component contracts, configuration boundary, runtime data, and tests, while source publication, tags, deployment, and releases follow OS Ecosystem.
9. **Backward-compatible contracts.** Additive changes are preferred; breaking public contract changes require a new API version.
10. **Approval-gated development.** No implementation begins until the Master Design, Architecture, and Structure pass review and receive explicit user approval.

## 5. Actors and boundaries

### Project callers

Living OS, Universal Learning Engine, and registered OS Ecosystem projects submit requests through the public AI Hub API. They own prompts, business context, user consent, and the use of returned content.

### Operators

Operators register providers and models, reference credentials, enable or disable resources, test connectivity, inspect health and usage, tune approved settings, and review sanitized execution evidence.

### Providers

OpenAI, Google Gemini, and Anthropic Claude are the initial provider families. xAI Grok and other providers are extensions implemented through the same adapter and registry contracts after approval.

### AI Hub authority

AI Hub owns request validation, routing, provider execution, normalized operational responses, provider health, usage accounting, predictions, settings, and execution logs. It does not own caller business data or caller-side actions.

## 6. Core modules

### 6.1 Dashboard

The Dashboard is a read-only operational summary showing:

- provider connection and enabled state
- registered and selected models
- current Online, Offline, Error, Disabled, or Unknown health
- last completed health check and observed response time
- recent call count, success rate, failure rate, and latency
- current measured usage and limit status when available
- router readiness, last routing decision, and failover count
- timestamps and data-source labels for every operational summary

The Dashboard never displays API keys, raw prompts, raw responses, or internal exception payloads.

### 6.2 Provider Management

Provider Management supports register, update, delete, enable, disable, and explicit connection test operations.

A provider registration contains a stable provider ID, provider family, display name, enabled state, credential reference, optional approved endpoint configuration, supported capabilities, and metadata. The credential value is resolved only at execution time through an approved secret source and is never returned by the API.

Deletion is rejected while a provider is referenced by an active model or protected policy. Historical execution records retain the provider ID after deletion. Connection tests are explicit operator actions, have a bounded timeout, and produce sanitized results.

### 6.3 Model Registry

Each model record contains:

- stable internal model ID
- provider ID and provider-native model name
- enabled and lifecycle state
- supported task kinds and structured-output capability
- configured context and output limits when known
- routing priority and task-suitability ratings
- observed health and usage references
- effective dates and operator notes

Models are explicitly registered and validated. AI Hub does not assume that a provider-advertised model is approved for ecosystem use.

### 6.4 AI Router

The router accepts a provider-neutral request and produces a recorded routing decision.

#### Hard eligibility gates

A candidate is excluded when any of the following applies:

- provider or model is disabled, deleted, or unregistered
- credential reference cannot be resolved
- health is Offline or administratively blocked
- task kind or required capability is unsupported
- request limits exceed configured model limits
- usage limit is exhausted or its safety threshold is crossed
- caller policy does not allow the candidate

`Unknown` health is eligible only when policy explicitly permits probe-on-use. A configured default provider never bypasses a hard gate.

#### Default ranking

Eligible candidates are ranked deterministically using normalized evidence:

| Signal | Default weight | Meaning |
| --- | ---: | --- |
| Health and availability | 30% | recent availability and check freshness |
| Task suitability | 25% | registered fit for the requested task kind |
| Remaining usage capacity | 20% | limit headroom or configured safe allowance |
| Response latency | 15% | bounded recent latency observation |
| Reliability | 10% | recent failure-rate evidence |

Missing evidence receives a conservative neutral or penalty value defined by policy; it is never silently treated as ideal. Ties are resolved by explicit routing priority and then stable model ID. Weights are versioned settings whose total must equal 100%.

When Auto Routing is disabled, the configured default provider and model are attempted if eligible. A caller-supplied provider hint is advisory and is accepted only for an authorized operational request; ordinary project callers cannot force a provider.

#### Failover

Failover occurs only for classified retryable failures such as timeout, transient connection failure, temporary provider failure, or eligible rate limiting. Authentication, permission, invalid request, safety rejection, and deterministic schema failures are not retried on the same provider unless policy explicitly classifies them otherwise.

The router never repeats a candidate that has already failed during the same request. Total attempts are bounded by `1 + retry_count`, the overall deadline, and the number of eligible candidates. Every attempt belongs to one correlation ID; the final response identifies the selected provider and model but never exposes credentials or raw provider errors.

### 6.5 Health Monitoring

Health Monitoring manages provider and model observations:

- `Online`: the latest valid check completed within the freshness window
- `Offline`: connection could not be established within policy
- `Error`: the provider responded but the check failed validation or authorization
- `Unknown`: no current evidence exists
- `Disabled`: operator configuration prevents checks and routing

Each observation records last check time, duration, outcome, sanitized code, and availability window. Passive execution evidence and active checks are stored separately. Active checks use minimal approved requests, bounded intervals, and no caller data.

### 6.6 Usage Analytics

Usage Analytics provides immutable aggregation over execution records by time range, caller project, provider, model, task kind, and outcome. Metrics include call and attempt counts, input/output units when reported, total usage units, mean and percentile latency, success rate, failure rate, retry count, and failover count.

Provider-reported usage and locally estimated usage remain distinguishable. Unknown values remain unknown rather than being converted to zero.

### 6.7 Usage Prediction

Usage Prediction estimates remaining free or configured allowance, expected limit time, and recommended provider-switch window. v0.1 uses deterministic calculations over recorded consumption and operator-entered or provider-reported limits.

Every prediction includes its generated time, evidence window, method version, confidence (`Insufficient`, `Low`, `Medium`, or `High`), and assumptions. Predictions are advisory inputs to routing policy; they do not purchase capacity, change accounts, or disable providers by themselves.

### 6.8 Settings

Settings manages:

- default provider and model
- Auto Routing enabled state
- retry count
- per-attempt and overall timeout
- health-check interval and freshness window
- routing weights and tie-breaking priority
- usage safety threshold
- unknown-health policy
- operational log retention policy

Settings changes are validated, versioned, attributed, timestamped, and auditable. Unsafe values such as negative timeouts, unbounded retries, or weights not totaling 100% are rejected.

### 6.9 API Management

API Management governs caller access to AI Hub, not provider credentials. It supports caller registration, scoped credential issuance or secret reference, enable/disable, rotation metadata, rate policy, and last-used evidence.

Caller credentials are hashed or secret-managed and are displayed only once when issuance requires it. Scopes distinguish inference, read-only operations, and administration. Living OS, Universal Learning Engine, and other projects receive separate identities.

### 6.10 Execution Log

Every request produces one immutable execution summary and zero or more attempt records.

Required request fields are correlation ID, timestamp, caller project, task kind, final provider, final model, total duration, attempt count, success, normalized error code, routing policy version, and usage metadata. Attempt records add sequence, provider, model, duration, outcome, and failover reason.

Raw prompt, response, API key, authorization header, and provider exception text are excluded by default. Diagnostic content retention requires a later explicit security and retention approval.

## 7. Public inference contract

### Request

The v0.1 request contains:

- caller-generated request ID for idempotency and traceability
- registered caller project identity
- task kind
- input messages or text in the approved neutral schema
- required response format: text or validated structured JSON
- optional schema for structured output
- maximum output limit
- deadline or timeout bounded by Hub policy
- non-sensitive tags for aggregation

Approved task kinds are `generation`, `reasoning`, `summarization`, `extraction`, `classification`, and `structured_generation`. New task kinds require a registry and contract update.

### Response

The normalized response contains:

- correlation ID and caller request ID
- status and normalized output
- selected provider ID and model ID
- total duration and attempt count
- normalized usage when available
- routing policy version
- retry/failover indicator
- sanitized error object on failure

Provider-native response objects do not cross the boundary. AI output remains untrusted content; callers must validate domain meaning and must require their own approval before any consequential action.

## 8. Error model

Stable categories are `invalid_request`, `unauthorized`, `forbidden`, `no_eligible_provider`, `credential_unavailable`, `timeout`, `rate_limited`, `provider_unavailable`, `provider_error`, `invalid_provider_response`, `usage_limit_reached`, and `internal_error`.

Errors expose a stable code, safe message, correlation ID, retryability, and attempt summary. Internal stack traces, provider payloads, secrets, and caller content are never returned through ordinary APIs.

## 9. Security and privacy

- Provider credentials and caller credentials live outside source control and ordinary data stores.
- Configuration stores secret references, never plaintext provider keys.
- Administrative actions require an administrator scope; dashboards default to read-only.
- Provider and caller network traffic uses authenticated encrypted transport in deployed environments.
- Logs are sanitized before persistence and access is auditable.
- Caller project identity is part of every request and usage record.
- Raw prompts and responses are transient by default and are not analytics inputs.
- Data sent to a provider is limited to the explicit request; AI Hub does not enrich it with another project's data.
- Credential rotation and incident revocation do not require code changes.

## 10. Reliability and operational requirements

- One request has one correlation ID across routing and all attempts.
- Idempotency prevents duplicate accepted work within the configured window when the caller repeats the same request ID.
- Per-attempt timeout cannot exceed the overall request deadline.
- Retry and failover are bounded and observable.
- Health and usage failure cannot corrupt provider configuration.
- Analytics and prediction failure cannot block ordinary inference when routing still has sufficient evidence.
- Administrative writes are transactional and leave an audit record.
- Startup validates configuration and registry consistency before declaring the router ready.
- Degraded readiness is visible when no eligible provider exists.

Quantitative service objectives are deployment decisions and must be approved before release; v0.1 design does not invent an uptime guarantee.

## 11. Data ownership and retention

AI Hub owns provider registrations, model registrations, routing policies, settings revisions, caller identities, health observations, usage aggregates, predictions, audit records, and sanitized execution metadata.

Callers own prompt content, response content, conversation history, learning evidence, and all domain records. AI Hub holds request content only for the duration needed to execute and normalize a call unless a separately approved retention mode exists.

Retention periods are configuration with approved defaults established during implementation review. Deletion of operational evidence must preserve required audit and referential integrity rules.

## 12. Administrative experience

The v0.1 operator interface contains Dashboard, Providers, Router, Health, Usage, Predictions, Models, API Management, Execution Log, and Settings. Destructive or security-sensitive actions require explicit confirmation. Every screen distinguishes configured state, measured state, estimated state, and stale or unavailable evidence.

The interface provides no free-form chat workspace.

## 13. Acceptance criteria

The design is eligible for implementation approval when:

- the ten core modules have explicit responsibilities and ownership
- public request, response, and error contracts are provider neutral
- initial OpenAI, Gemini, and Claude adapters can fit without leaking SDK types
- hard routing gates, ranking, tie-breaking, retry, and failover are deterministic
- default provider behavior cannot bypass health, capability, or usage gates
- provider keys and caller credentials cannot appear in UI, logs, or source
- raw prompt and response retention is disabled by default
- health, analytics, and prediction distinguish measured, estimated, stale, and unknown data
- Living OS and Universal Learning Engine remain independently deployable and retain their data ownership
- the repository plan separates domain, application, infrastructure, presentation, tests, data, and configuration
- Design Review records no unresolved blocking issue
- explicit user approval is recorded before implementation begins

## 14. Required lifecycle

1. Master Design — document product boundary and contracts.
2. Design Review — inspect completeness, risks, consistency, and testability.
3. Approval — record explicit user authorization and approved document revisions.
4. Implementation — build only the approved scope.
5. Testing — validate contracts, failure handling, security boundaries, and UI.
6. Release — version, publish evidence, deploy, and verify only after approval.

The design approval gate was completed on 2026-07-22. Implementation may now proceed only through an implementation plan mapped to these acceptance criteria. Real credentials, deployment, testing completion claims, and release remain subject to their own controls.
