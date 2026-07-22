# AI Hub v0.1 Architecture

Status: v0.1 Final
Approval: Approved on 2026-07-22
Implementation: Complete; included in OS Ecosystem v0.6.2

## 1. System placement

```text
User
  -> OS Ecosystem
      -> Living OS / Universal Learning Engine / approved project
          -> AI Hub Public API
              -> Request Validation and Caller Authorization
                  -> AI Router
                      -> Provider Adapter
                          -> OpenAI / Gemini / Claude / extension provider
                      <- Provider-native response
                  <- Normalized response
          <- Caller-owned validation and action
```

AI Hub is an official common platform component inside the OS Ecosystem repository. It is the shared inference operations boundary, not a separate repository or service and not part of Living OS or Universal Learning Engine persistence.

## 2. Architectural style

AI Hub uses a modular service architecture with ports and adapters:

- **Presentation:** operator UI and transport endpoints
- **Application:** use cases, authorization, orchestration, and transaction boundaries
- **Domain:** provider-neutral contracts, routing policy, health, usage, prediction, registries, and errors
- **Infrastructure:** provider SDK adapters, secret resolver, database repositories, clock, and telemetry

Dependencies point inward. Domain code imports no provider SDK, web framework, UI framework, database driver, or caller project. Provider adapters implement domain ports and are replaceable.

## 3. Control plane and data plane

### Control plane

Dashboard, Provider Management, Model Registry, Health Monitoring, Usage Analytics, Usage Prediction, Settings, API Management, and audit views manage configuration and operational evidence.

### Data plane

The Public Inference API, request validator, caller authorizer, router, attempt coordinator, provider adapters, response normalizer, and execution recorder process inference calls.

The control plane may change approved configuration. It never edits a caller's business records. The data plane reads an immutable settings/policy snapshot for each request so mid-request administrative changes cannot create inconsistent routing.

## 4. Major components

| Component | Responsibility | Must not own |
| --- | --- | --- |
| Public API | stable versioned request/response transport | provider SDK objects |
| Caller Auth | identity, scope, enabled and rate policy checks | provider credentials |
| Request Validator | neutral schema, limits, task and deadline validation | routing choice |
| Router | eligibility, scoring, tie-break, candidate plan | provider network execution |
| Attempt Coordinator | deadline, retry, failover, final outcome | business interpretation |
| Provider Port | neutral execution and health contracts | SDK implementation |
| Provider Adapters | SDK mapping, timeouts, usage extraction, error classification | global routing policy |
| Provider Registry | provider identity and enabled configuration | plaintext secrets |
| Model Registry | model capability and lifecycle metadata | automatic approval |
| Health Service | active and passive observations, freshness | provider configuration mutation |
| Usage Service | normalized immutable observations and aggregates | fabricated missing values |
| Prediction Service | deterministic allowance projections | autonomous purchasing |
| Execution Recorder | sanitized request and attempt evidence | raw content by default |
| Settings Service | validated, versioned policy snapshots | unbounded values |
| Secret Resolver | runtime credential resolution | displaying or logging secrets |
| Operator UI | management commands and read models | direct repository or SDK access |

## 5. Core ports

### Inference service port

`execute(request, caller_context) -> normalized_response`

The port owns validation-to-final-record orchestration and returns one final outcome.

### Provider adapter port

```text
execute(neutral_request, model_registration, credential, deadline)
  -> provider_result | classified_provider_error

check_health(provider_registration, credential, deadline)
  -> health_observation
```

An adapter must enforce the supplied deadline, translate the neutral request, normalize text/structured output and usage, sanitize errors, and return no SDK object.

### Repository ports

Separate ports own providers, models, settings revisions, callers, health observations, usage observations, execution summaries, attempts, predictions, and audit records. Cross-domain writes occur through application services and one explicit transaction boundary where atomicity is required.

### Secret resolver port

`resolve(secret_reference) -> short_lived_secret`

The secret is held only for the outbound call scope and is never persisted by AI Hub repositories.

## 6. Inference sequence

```text
Caller -> Public API: neutral request + caller credential
Public API -> Caller Auth: authenticate and authorize
Public API -> Request Validator: validate schema and bounds
Request Validator -> Settings: capture policy snapshot
Settings -> Router: request + eligible registry/health/usage evidence
Router -> Attempt Coordinator: ordered candidate plan + reasons
Attempt Coordinator -> Secret Resolver: resolve candidate credential
Attempt Coordinator -> Provider Adapter: execute with deadline
Provider Adapter -> Attempt Coordinator: result or classified error
Attempt Coordinator -> Execution Recorder: sanitized attempt
Attempt Coordinator -> Provider Adapter: next eligible candidate if allowed
Attempt Coordinator -> Execution Recorder: final execution summary
Attempt Coordinator -> Public API: normalized final response
Public API -> Caller: response
```

No attempt begins after the overall deadline. Final recording is best-effort fail-safe: a recording fault is surfaced operationally but cannot convert a successfully received provider response into a second provider execution.

## 7. Routing architecture

Routing has four stages:

1. **Capability match:** task kind, response format, context/output bounds, and caller policy.
2. **Operational eligibility:** enabled state, credential availability, health policy, and usage limits.
3. **Deterministic ranking:** approved policy version, normalized evidence, stable tie-break.
4. **Attempt plan:** unique candidates bounded by retry count and deadline.

The router stores a decision record containing policy version, considered candidate IDs, exclusion reason codes, score components, final order, and decision timestamp. It stores no prompt content.

Adapters classify failures into the common error model. The Attempt Coordinator, not an adapter, decides whether to retry or fail over.

## 8. Health architecture

Active checks are scheduled administrative operations and use provider-specific minimal probes behind the adapter port. Passive observations originate from ordinary execution attempts. The Health Service calculates current state from the newest valid evidence and its freshness window without changing provider enabled state.

A monitor outage produces stale or Unknown health, not a fabricated Online result. Health-check execution uses separate rate controls so it cannot consume unbounded inference allowance.

## 9. Usage and prediction architecture

Provider adapters emit normalized usage observations where available, preserving provider units and source. The Usage Service creates projections without rewriting immutable observations. Aggregates are reproducible from source records.

The Prediction Service consumes time-bounded observations and registered allowance rules. Each result stores the method version and assumptions. Predictions are recalculated; they are never treated as provider truth when derived locally.

## 10. Persistence model

The initial logical stores are:

- `provider_registrations`
- `model_registrations`
- `caller_registrations`
- `settings_revisions`
- `routing_decisions`
- `health_observations`
- `usage_observations`
- `usage_predictions`
- `execution_summaries`
- `execution_attempts`
- `audit_records`

Identifiers are stable and timestamps use UTC internally. Records reference provider/model IDs rather than mutable display names. Schema migrations are additive, versioned, idempotent, tested, and never run against production without release authorization and a rollback plan.

Runtime data belongs under `data/` and is never committed. Configuration examples belong under `config/`; real credentials do not.

## 11. API boundaries

### Project API

- versioned inference endpoint
- caller-scoped request status or trace lookup using sanitized metadata
- health/readiness endpoint with no internal or provider-sensitive details

### Administrative API

- provider and model lifecycle
- explicit connection and health tests
- settings revisions
- caller identity lifecycle
- dashboards, analytics, predictions, and execution queries

Administrative and project scopes are separate. A project caller cannot change routing configuration or inspect another caller's evidence.

## 12. Security boundaries

1. Transport authenticates before request content reaches routing.
2. Authorization binds caller identity, scopes, limits, and visibility.
3. Secret resolution occurs after candidate selection and immediately before execution.
4. Sanitization occurs before errors or records cross an adapter boundary.
5. Operator UI consumes administrative application services only.
6. Persistence excludes plaintext credentials and raw inference content by default.
7. Audit records cover administrative state changes without copying secret values.

## 13. Caller integration contract

Living OS and Universal Learning Engine depend only on an AI Hub client port or versioned public contract. They do not import AI Hub infrastructure or provider adapters. Each caller:

- supplies its registered project identity
- validates domain inputs before submission
- treats model output as untrusted
- owns user-facing error behavior and domain validation
- obtains user approval for consequential actions
- stores any desired conversation or result history in its own domain

AI Hub has no callback that can directly mutate caller data.

## 14. Extension contract

A new provider requires:

- a new adapter implementing the existing provider port
- sanitized error mappings
- health-check behavior
- usage normalization behavior
- capability and model registrations
- contract, failure, timeout, and secret-leak tests
- explicit approval before enablement

Adding an adapter must not require changes to the public inference contract, Router domain rules, or existing adapters.

## 15. Deployment boundary

AI Hub deploys with OS Ecosystem in the same Streamlit application. Deployment configuration supplies database location, secret-source settings, allowed callers, and operational policy. No separate AI Hub deployment address, provider key, or environment-specific value is hardcoded in source.

The operator UI and API may share a process in v0.1 only if their module and authorization boundaries remain separate. Distributed workers, message brokers, and multi-region coordination are deferred.

## 16. Test architecture requirements

- pure Router unit tests for every gate, score, tie, and missing-evidence case
- adapter contract tests using fakes; no credential required for default test suite
- failure-classification, retry, failover, timeout, and idempotency tests
- repository and migration tests with isolated temporary data
- authorization and cross-caller isolation tests
- secret and raw-content non-disclosure tests for API, UI, and logs
- usage aggregation and deterministic prediction tests
- UI tests for status provenance, stale evidence, confirmation, and accessibility
- integration tests for Living OS and Universal Learning Engine client contracts
- optional live-provider smoke tests only with explicit credentials and approval

## 17. Architecture decisions proposed for approval

- AI Hub is an OS Ecosystem-owned official common platform component.
- The primary interface is provider-neutral and machine-to-machine.
- v0.1 supports text and structured JSON tasks only.
- Ports-and-adapters boundaries isolate provider SDKs.
- Routing is deterministic, evidence-based, versioned, and explainable.
- Control plane and data plane are logically separate.
- Raw prompt and response content is transient by default.
- Initial persistence is one AI Hub component-owned relational store behind repositories and inside the approved runtime-data boundary.
- Synchronous request execution is the v0.1 baseline; distributed execution is deferred.
