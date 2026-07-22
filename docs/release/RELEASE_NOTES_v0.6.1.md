# OS Ecosystem v0.6.1 Release Notes

Release date: 2026-07-22

OS Ecosystem v0.6.1 registers AI Hub as an official independent ecosystem project beside Living OS and Universal Learning Engine.

## AI Hub project entry

- Added an AI Hub card to the integrated launcher.
- Added AI Hub to the top navigation.
- Added a responsive AI Hub entry screen with version, routing, provider, and operations summaries.
- Added AI Hub v0.1.0 Release Candidate to the project and version registries.
- Added optional `AI_HUB_URL` configuration. Safe HTTP(S) destinations open the independent dashboard; otherwise the launcher uses its internal AI Hub entry screen.

## Compatibility

- Living OS and Universal Learning Engine URLs and independent runtimes are unchanged.
- Existing capability contracts, registries, and launcher sections remain compatible.
- AI Hub runtime source, credentials, Provider validation, release, and deployment remain outside this OS Ecosystem patch.

## Security

- No API Key, Token, credential, or deployment secret is included.
- `.env` and Streamlit runtime secrets remain ignored.
- External project destinations continue to require validated HTTP(S) URLs.

## Validation

- Launcher and documentation contract tests.
- Safety, Enhancement, Automation, Collaboration & Connectivity, and Personal Secretary regression tests.
- AI Hub local test suite.
- Desktop and 390px mobile launcher verification.
- Production verification after GitHub Release publication and Streamlit redeployment.

## Deployment

- Production: https://8javbq85jtappi6tkdhkt7g.streamlit.app/
- Deployment follows merge to `main`, immutable `v0.6.1` tag publication, GitHub Release creation, and production validation.
