# Safety Capability v1.0

Safety Capability is an independent, reusable execution foundation for common safety functions in the OS Ecosystem. Version 1.0 stabilizes its public contracts, routing, failure isolation, execution records, health reporting, and artifact deployment contract. It is a foundation, not a complete safety product.

## Architectural position

```text
OS Ecosystem
├── Capability Layer
│   └── Safety Capability (this project)
└── Module Layer
    ├── Living OS
    ├── Universal Learning Engine
    └── future modules
```

The capability sits above modules. A module sends a `SafetyRequest` through the public interface and consumes a `SafetyResult`; the capability does not own module business logic, and modules do not access capability internals.

## Included in v1.0

- Common execution context, request, and result schemas
- Replaceable `SafetyComponent` interface
- Component registration, duplicate prevention, action lookup, enabled state, version, and health
- Context/input/output validation and isolated component execution
- Stable error-code conversion and explicit failure results
- Success and failure persistence through a replaceable repository
- SQLite execution database adapter
- Capability and per-component health reporting
- Basic validation test component and executable example
- Automated tests and design/integration contracts
- Documented consumer, extension, and private API boundaries
- Runtime recovery and deployment rollback responsibility boundaries
- GitHub Release artifact and clean-install deployment gate

## Requirements and installation

Python 3.11 or newer is required. From this directory:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -e ".[dev]"
```

The runtime itself has no third-party dependencies. The `dev` extra installs pytest.

## Run the example

```powershell
python app.py
```

The example creates a runtime, registers `BasicValidationComponent`, sends a `validate` request, prints the common result, confirms the database record, and prints capability/component health. Runtime data is written to `data/safety_executions.db` and ignored by Git.

## Minimal use

```python
from safety_capability import (
    BasicValidationComponent,
    SafetyExecutionContext,
    SafetyRequest,
    SafetyRuntime,
)

with SafetyRuntime() as runtime:
    runtime.registry.register(BasicValidationComponent())
    context = SafetyExecutionContext(
        source="my-module",
        target="sample-operation",
        action="validate",
        payload={"value": 42},
    )
    result = runtime.execute(SafetyRequest(context))
    if result.success:
        print(result.details)
    else:
        print(result.error_code, result.message)
```

An explicit component can be selected with `SafetyRequest(context, component_id="basic-validation")`. Without one, the registry deterministically selects the first enabled component that supports the action.

Passing an object other than `SafetyRequest` is a caller programming error and raises `TypeError`. Once a valid request enters execution, validation, routing, component, and repository failures are returned through the stable result contract whenever a result can be formed.

## Run tests

```powershell
python -m pytest
```

The suite covers normal runtime execution, context and result contracts, registration and duplicate blocking, discovery, disabled components, unsupported actions, invalid input, failure isolation, error codes, records, database recreation, and health reporting.

## Deployment

Safety Capability is not a Streamlit or service deployment. Deployment means publishing immutable wheel and source artifacts in a namespaced GitHub Release, installing the wheel in a clean supported Python environment, and verifying import, runtime execution, persistence, controlled errors, and health. See `docs/DEPLOYMENT_CONTRACT.md`.

Runtime rollback is not a v1.0 Core function. Operational deployment rollback selects a previously verified artifact and OS Ecosystem manifest entry. See `docs/RECOVERY_POLICY.md`.

## Project structure

```text
Safety-Capability/
├── app.py
├── docs/                    architecture and public contracts
├── src/safety_capability/
│   ├── core/                context, result, errors, health, runtime
│   ├── interfaces/          component abstraction
│   ├── registry/            component catalog and state
│   ├── execution/           executor and failure isolation
│   ├── database/            repository contract and SQLite adapter
│   └── components/          basic v1.0 verification component
├── tests/
└── data/                    local runtime records
```

## Documentation

- `docs/ARCHITECTURE.md`: ecosystem position, flow, dependencies, boundaries
- `docs/MASTER_DESIGN.md`: goals, model, selection, failures, evolution
- `docs/INTERFACE_CONTRACT.md`: component obligations
- `docs/MODULE_INTEGRATION_CONTRACT.md`: allowed future module boundary
- `docs/EXECUTION_DATABASE_CONTRACT.md`: storage adapter contract
- `docs/PUBLIC_API.md`: consumer, extension, and private boundaries
- `docs/RECOVERY_POLICY.md`: runtime recovery and deployment rollback responsibilities
- `docs/DEPLOYMENT_CONTRACT.md`: artifact and clean-install release gate
- `docs/ARCHITECTURE_RELEASE_GATE.md`: v1.0 Architecture Gate decision and evidence
- `docs/ROADMAP.md`: candidate future phases
- `docs/RELEASE_CHECKLIST.md`: local release-readiness checks

## Limitations

v1.0 is synchronous and single-process, uses basic deterministic routing, and does not guarantee recording if the repository itself is unavailable. It contains no production safety policy, runtime rollback or recovery engine, external monitoring, authentication, AI risk decisions, automatic intervention, Personal Secretary or AI Hub integration, official UI, or dashboard.

There is intentionally no direct Living OS, Universal Learning Engine, Investment OS, or Job OS integration in this version.

## Roadmap

Likely next steps are richer routing/configuration and observability, followed by opt-in recovery strategies and asynchronous execution. Real module adapters belong to a separately approved integration phase. See `docs/ROADMAP.md`.
