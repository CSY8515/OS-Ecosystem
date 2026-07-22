# AI Hub v0.1 Repository Structure — Final

Version: v0.1 Final
Status: Approved
Approved: 2026-07-22
Implementation stage: Complete; included in OS Ecosystem v0.6.2

## 1. Purpose

This document is the authoritative component structure contract for AI Hub v0.1 inside the OS Ecosystem repository. It preserves the requested `docs`, `src`, `tests`, `data`, and `config` boundaries while applying documentation-first, independently testable, adapter-based standards.

## 2. Official top-level structure

```text
AI-Hub/
  README.md
  VERSION
  pyproject.toml
  .gitignore
  docs/
  src/
  tests/
  data/
  config/
```

| Path | Authority |
| --- | --- |
| `docs/` | design, architecture, contracts, review, operations, testing, and release evidence |
| `src/` | production implementation only |
| `tests/` | automated verification and test fixtures only |
| `data/` | AI Hub-owned local runtime data only |
| `config/` | safe configuration examples and schemas only |

Component root files provide entry, version, packaging, and ignore rules within OS Ecosystem. Production secrets, generated reports, caches, and runtime logs are never committed.

## 3. Official complete layout

```text
AI-Hub/
  README.md
  VERSION
  pyproject.toml
  .gitignore
  docs/
    MASTER_DESIGN.md
    ARCHITECTURE.md
    STRUCTURE.md
    DESIGN_REVIEW.md
    APPROVAL.md
    API_CONTRACT.md
    PROVIDER_ADAPTER_CONTRACT.md
    ROUTING_POLICY.md
    DATA_CONTRACT.md
    SECURITY.md
    OPERATIONS.md
    TEST_PLAN.md
    RELEASE_CHECKLIST.md
    releases/
  src/
    ai_hub/
      __init__.py
      application/
        inference_service.py
        provider_management_service.py
        model_registry_service.py
        health_service.py
        usage_analytics_service.py
        usage_prediction_service.py
        execution_log_service.py
        settings_service.py
        api_management_service.py
        dashboard_query_service.py
      domain/
        common/
          contracts.py
          errors.py
          identifiers.py
          types.py
        router/
          models.py
          eligibility.py
          scoring.py
          policy.py
          service.py
        providers/
          entities.py
          capabilities.py
          ports.py
        models/
        health/
        usage/
        predictions/
        executions/
        settings/
        callers/
        audit/
      infrastructure/
        providers/
          openai/
            adapter.py
            mapper.py
            errors.py
          gemini/
            adapter.py
            mapper.py
            errors.py
          claude/
            adapter.py
            mapper.py
            errors.py
        persistence/
          database.py
          repositories/
          migrations/
        secrets/
        telemetry/
        scheduling/
        clock.py
      presentation/
        api/
          routes/
          schemas/
          dependencies.py
        operator_ui/
          pages/
            dashboard.py
            providers.py
            router.py
            health.py
            usage.py
            predictions.py
            models.py
            api_management.py
            execution_log.py
            settings.py
          components/
          navigation.py
      bootstrap/
        container.py
        configuration.py
        readiness.py
      utilities/
        redaction.py
        serialization.py
        timestamps.py
        validation.py
  tests/
    unit/
      domain/
      application/
      utilities/
    contract/
      provider_adapters/
      public_api/
    integration/
      persistence/
      providers/
      callers/
    security/
    ui/
    smoke/
    fixtures/
  data/
    .gitkeep
  config/
    settings.example.yaml
    logging.example.yaml
```

Framework, database library, and operator-UI technology remain implementation-plan decisions. They must fit these boundaries and cannot redefine them implicitly.

## 4. Core module placement

| Required module | Canonical owner | Presentation |
| --- | --- | --- |
| Dashboard | `application/dashboard_query_service.py` | `presentation/operator_ui/pages/dashboard.py` |
| Provider Management | `application/provider_management_service.py` | `presentation/operator_ui/pages/providers.py` |
| AI Router | `domain/router/` | `presentation/operator_ui/pages/router.py` |
| Provider Adapter | `domain/providers/ports.py` and `infrastructure/providers/` | managed through Providers |
| Health Monitoring | `domain/health/`, `application/health_service.py` | `presentation/operator_ui/pages/health.py` |
| Usage Analytics | `domain/usage/`, `application/usage_analytics_service.py` | `presentation/operator_ui/pages/usage.py` |
| Usage Prediction | `domain/predictions/`, `application/usage_prediction_service.py` | `presentation/operator_ui/pages/predictions.py` |
| Execution Log | `domain/executions/`, `application/execution_log_service.py` | `presentation/operator_ui/pages/execution_log.py` |
| Settings | `domain/settings/`, `application/settings_service.py` | `presentation/operator_ui/pages/settings.py` |
| Utilities | `utilities/` | no page and no business authority |
| Model Registry | `domain/models/`, `application/model_registry_service.py` | `presentation/operator_ui/pages/models.py` |
| API Management | `domain/callers/`, `application/api_management_service.py` | `presentation/operator_ui/pages/api_management.py` |

Model Registry and API Management are retained because they are approved AI Hub core modules even though they were omitted from the abbreviated `src` list in the structure request.

## 5. Provider adapter contract

The Router depends only on the provider port in `domain/providers/ports.py`. It never imports OpenAI, Gemini, Claude, or a future provider package.

Each provider has one independent directory containing:

- `adapter.py`: provider-port implementation
- `mapper.py`: neutral request/response and usage translation
- `errors.py`: provider-native to stable error classification

An adapter may depend on its own provider SDK and neutral domain contracts. It may not import another provider adapter, choose the next provider, change global routing weights, access operator UI state, or persist caller business data.

Adding Grok or another provider requires a sibling directory under `infrastructure/providers/`, contract tests, registry metadata, and approval. It requires no change to Router domain code or the public inference contract.

## 6. Router ownership rule

`domain/router/` is the sole authority for candidate eligibility, evidence normalization, scoring, tie-breaking, and ordered attempt plans.

- `eligibility.py` applies hard exclusion gates.
- `scoring.py` calculates approved weighted scores.
- `policy.py` represents immutable versioned routing policy.
- `service.py` produces the routing decision and candidate order.
- `models.py` defines provider-neutral routing inputs and results.

Retry and failover execution is orchestrated by `application/inference_service.py`; adapters only report normalized results or classified errors. This prevents Provider code from becoming a second Router.

## 7. Health, usage, and execution ownership

### Health

`domain/health/` defines Online, Offline, Error, Unknown, and Disabled states plus response time, availability, last check, evidence source, and freshness. `application/health_service.py` coordinates active and passive observations. Scheduling mechanics belong to `infrastructure/scheduling/`.

### Usage

`domain/usage/` owns immutable usage observations and aggregation rules. `domain/predictions/` owns deterministic prediction results, evidence windows, assumptions, and confidence. Unknown usage is never rewritten as zero.

### Execution

`domain/executions/` owns one final execution summary and its attempt records. The persisted contract includes Timestamp, Provider, Model, Task, Duration, Success, sanitized Error, Retry count, correlation ID, caller ID, usage, routing-policy version, and failover evidence. Raw prompts, responses, keys, and provider exception payloads are excluded by default.

## 8. Settings and API management ownership

`domain/settings/` owns validated Default Provider, Auto Routing, Retry, Timeout, Health Check Interval, routing weights, usage threshold, and retention settings. Settings are versioned and immutable once used by an execution.

`domain/callers/` and `application/api_management_service.py` own AI Hub caller identities, scopes, enablement, rotation metadata, and rate policy. Provider API keys remain behind `infrastructure/secrets/`; caller access credentials and provider credentials are never mixed.

## 9. Layer ownership rules

### `docs/`

All authoritative development documents live here. Uppercase snake case is used for authoritative filenames. `docs/releases/` contains version-specific release evidence. Package-local comments or READMEs cannot replace a central contract.

### `application/`

Coordinates use cases, authorization, transactions, retry/failover execution, and queries. It depends on domain contracts and injected ports, never concrete SDKs, database drivers, or UI state.

### `domain/`

Owns provider-neutral policy and types. It cannot import presentation, infrastructure, provider SDKs, Living OS, Universal Learning Engine, or OS Ecosystem runtime code.

### `infrastructure/`

Implements external ports for providers, persistence, secrets, telemetry, scheduling, and time. It owns mechanics, not global business policy.

### `presentation/`

Maps transport and operator UI to application services. It owns no canonical policy, persistence, secret resolution, or direct provider call.

### `bootstrap/`

Is the only composition root. It validates configuration, creates concrete implementations, wires ports, and publishes readiness.

### `utilities/`

Contains small stateless technical helpers used by more than one layer. It may contain redaction, serialization, timestamp, and syntax validation helpers. Routing rules, provider logic, persistence access, credentials, mutable global state, and domain decisions are prohibited. A helper used by only one module remains in that module.

## 10. Dependency contract

```text
presentation -> application -> domain
bootstrap -> presentation + application + infrastructure + domain
infrastructure -> domain ports
utilities -> standard-library-only technical helpers
domain -> no outer layer
```

Production code never imports from `tests/`, `data/`, or another OS Ecosystem project. Living OS and Universal Learning Engine use only the versioned public AI Hub contract governed by OS Ecosystem.

## 11. Test structure and gates

- `unit/`: deterministic domain, application, and utility behavior
- `contract/provider_adapters/`: one shared suite every provider adapter must pass
- `contract/public_api/`: request, response, error, and compatibility contracts
- `integration/persistence/`: repositories, transactions, migrations, backup, and restore
- `integration/providers/`: opt-in fake or approved live-provider integration
- `integration/callers/`: Living OS and Universal Learning Engine boundaries
- `security/`: authorization, caller isolation, redaction, secret, and raw-content tests
- `ui/`: dashboard and management behavior, accessibility, and safe rendering
- `smoke/`: startup, readiness, and supported-runtime verification
- `fixtures/`: synthetic, non-secret evidence only

Default tests use fakes and temporary storage and require no external credential or paid provider call. A new provider is incomplete until it passes the common adapter contract suite.

## 12. Data, configuration, and migration rules

- Runtime writes remain under the configured `data/` boundary or approved external store.
- Reads do not silently create or migrate production storage.
- Migrations are additive, versioned, idempotent, isolated, and explicitly invoked.
- Backup, restore, rollback, integrity verification, and retention are documented before the first production migration.
- Test state uses isolated temporary paths.
- `config/` contains examples and schemas, never real keys, caller secrets, database credentials, or deployment addresses.
- Configuration resolution preserves explicit deployment values and validates registry references, weights, retry bounds, timeouts, and intervals at startup.

## 13. Review findings incorporated

The Repository Structure review found no blocker after incorporating these improvements:

1. Added Model Registry and API Management omitted from the abbreviated source list.
2. Separated provider-neutral ports from provider SDK adapters.
3. Made Router the only routing-policy authority and kept retry orchestration outside adapters.
4. Added Security/Audit, persistence migrations, secret resolution, telemetry, scheduling, and readiness boundaries.
5. Added shared provider adapter contract tests and cross-caller isolation tests.
6. Restricted Utilities to stateless technical helpers to prevent an unowned catch-all module.
7. Preserved runtime data, configuration, documentation, implementation, and test placement rules.

These changes make provider addition additive and preserve Living OS and Universal Learning Engine independence.

## 14. Finalization and change control

This structure is **Repository Structure v0.1 Final**. Implementation may create the approved runtime directories and files only through an implementation plan mapped to the Master Design acceptance criteria.

Additive internal files may be introduced within the approved owners. Changes to the top-level boundaries, dependency direction, Router authority, provider adapter contract, public API ownership, credential boundary, or caller data ownership require a new Design Review and explicit approval.
