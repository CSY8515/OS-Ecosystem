# OS Ecosystem v0.6.1 Release Notes

> Ownership correction: v0.6.2 supersedes the independent AI Hub repository/service assumptions in this historical release note. AI Hub is an OS Ecosystem-owned common platform component.

Release date: 2026-07-22

OS Ecosystem v0.6.1 introduced AI Hub as an official ecosystem entry beside Living OS and Universal Learning Engine.

## AI Hub project entry

- Added an AI Hub card to the integrated launcher.
- Added AI Hub to the top navigation.
- Added a responsive AI Hub entry screen with version, routing, provider, and operations summaries.
- Added AI Hub v0.1.0 to the project and version registries as an initial entry candidate.
- Added an initial internal AI Hub entry screen; v0.6.2 replaced its provisional external-dashboard concept with the integrated repository route.

## Compatibility

- Living OS and Universal Learning Engine URLs and independent runtimes are unchanged.
- Existing capability contracts, registries, and launcher sections remain compatible.
- AI Hub runtime source was not included in this patch and was subsequently integrated by v0.6.2. Credentials remain deployment secrets.

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
