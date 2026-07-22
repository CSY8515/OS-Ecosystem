# AI Hub v0.1 Operations

Status: Local implementation baseline

## Verify

```text
python -m pytest
python -m compileall -q src tests
```

## Start the Dashboard

Set `PYTHONPATH=src`, then run:

```text
python -m streamlit run src/ai_hub/presentation/operator_ui/app.py --server.headless true
```

## Storage

Resolve `RuntimeConfiguration`, explicitly run required repository migrations, then start application services. Never place real secrets in `config/`. Provider SDKs are installed through the matching optional dependency group.

## Incident rule

Disable the affected Provider registration, revoke or rotate the external credential, retain sanitized correlation evidence, and do not copy raw caller content into incident logs.
