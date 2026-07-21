# OS Ecosystem Architecture

Version: v0.2.1

## Purpose

OS Ecosystem is a navigation shell, not a shared application runtime. It gives users one entry point while preserving the autonomy of every connected project.

## Runtime flow

1. Streamlit loads the launcher and its public project catalog.
2. The launcher resolves each destination from Streamlit Secrets, environment variables, or an approved default.
3. The UI renders only project identity, a short purpose statement, and connection status.
4. A user selects a project node.
5. The browser navigates to that project's independent UI.

## Boundaries

### Public launcher layer

- Central ecosystem identity
- Project nodes
- Project descriptions
- Destination links
- Connection availability

### Hidden operational layer

- Project capabilities and feature registries
- Databases, schemas, and storage
- Runtime processes and execution contracts
- Credentials and deployment secrets
- Integration adapters and internal health data

The hidden layer may support operation, but it must not become launcher navigation or dashboard content.

## Independence contract

Living OS and Universal Learning Engine retain their own UI, source boundaries, versions, tests, releases, persistence, and deployment lifecycles. OS Ecosystem does not import either application or read/write their data.

## Configuration and security

- Only validated `http` or `https` destinations are rendered.
- Secrets are never embedded in links or displayed in the interface.
- Invalid or missing project destinations render as unavailable nodes.
- Navigation is user-initiated; the launcher performs no background project execution.

## Deployment

OS Ecosystem is deployed as its own Streamlit application. Each project is deployed independently, and its production URL is supplied to the launcher through deployment configuration.
