# AI Hub

Component version: v0.1.0
Ecosystem release: OS Ecosystem v0.6.2
Lifecycle status: Integrated common platform
Implementation status: Complete; live Provider availability depends on deployment secrets

AI Hub is the shared AI operations platform for OS Ecosystem. Ecosystem projects submit provider-neutral requests; AI Hub selects an eligible provider and model, executes the request, records operational evidence, and fails over when policy permits.

AI Hub is not a general-purpose chat application. Its direct interface exists for operations and administration.

## Authoritative design set

- [Master Design](docs/MASTER_DESIGN.md)
- [Architecture](docs/ARCHITECTURE.md)
- [Repository Structure](docs/STRUCTURE.md)
- [Design Review](docs/DESIGN_REVIEW.md)
- [Approval Record](docs/APPROVAL.md)
- [API Contract](docs/API_CONTRACT.md)
- [Provider Adapter Contract](docs/PROVIDER_ADAPTER_CONTRACT.md)
- [Routing Policy](docs/ROUTING_POLICY.md)
- [Security](docs/SECURITY.md)
- [Operations](docs/OPERATIONS.md)
- [Test Plan](docs/TEST_PLAN.md)
- [Implementation Report](docs/IMPLEMENTATION_REPORT.md)
- [Release Checklist](docs/RELEASE_CHECKLIST.md)
- [Release Runbook](docs/RELEASE_RUNBOOK.md)
- [Release Review v0.1](docs/RELEASE_REVIEW_v0.1.md)

## Required lifecycle

`Master Design -> Design Review -> Approval -> Implementation -> Testing -> Release`

The approved v0.1 implementation is included in the OS Ecosystem repository and release lifecycle. The default test suite uses fake providers and temporary data; no real credential or paid provider call is required. Missing deployment credentials produce explicit unavailable Provider state and do not remove the integrated platform from the ecosystem release.

## Local verification

```text
python -m pytest
python -m compileall -q src tests
```

Integrated operator dashboard startup:

```text
streamlit run ../app.py
```

Open `?project=ai-hub` from the launcher card or top navigation. The package-local operator entry point remains a test fixture and development aid, not an independent deployment.
