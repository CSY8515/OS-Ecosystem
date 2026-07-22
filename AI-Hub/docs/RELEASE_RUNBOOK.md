# AI Hub v0.1 Integrated Operations Runbook

Status: Included in OS Ecosystem v0.6.2

## 1. Repository release

AI Hub source is reviewed, tested, tagged, released, and deployed only through the OS Ecosystem repository workflow. Do not create an AI Hub repository, external URL, independent tag, independent GitHub Release, or separate deployment.

## 2. Secret configuration

Configure Provider keys and approved models only through ignored `.env`, Streamlit Secrets, or deployment environment variables. Never commit or print values.

- `AI_HUB_OPENAI_API_KEY` and `AI_HUB_OPENAI_MODEL`
- `AI_HUB_GEMINI_API_KEY` and `AI_HUB_GEMINI_MODEL`
- `AI_HUB_CLAUDE_API_KEY` and `AI_HUB_CLAUDE_MODEL`

## 3. Credential-free verification

From `AI-Hub/`:

```text
python -m pytest
python -m compileall -q src tests
```

From the repository root, run the full OS Ecosystem suite and verify the internal `?project=ai-hub` route.

## 4. Optional live Provider activation

With explicit authorization and deployment secrets available:

```text
python -m ai_hub.bootstrap.release_validation --live
```

The validation lists models, checks approved selections, performs bounded probes and inference, verifies Router behavior, and writes sanitized evidence. It never prints credentials or model output.

## 5. Failure rule

Missing or invalid Provider configuration produces explicit unavailable readiness. It must not fall back to a separate service or external dashboard and must not alter the OS Ecosystem architecture.
