# Security Considerations

Version: v1.0.0

- API keys, tokens, passwords, and personal authentication data must not be hardcoded.
- Public documents and examples contain no real credentials.
- Execution records exclude request headers and full payloads.
- Secret-shaped metadata keys are redacted before recording.
- Provider authentication is represented by an interface and metadata classification; v1.0 does not ship a production OAuth implementation.
- Request size, connector enabled state, allowed operation, risk level, and response identity pass through Safety validation.
- Critical-risk external execution is blocked by the default local gateway.
- Environment variables, deployment secrets, or a future secret-provider adapter may supply credentials to a provider without changing the connector contract.
- Provider implementations must minimize payload retention and use destination-specific authorization.

Security controls are additive. A provider adapter cannot weaken application authorization or Safety governance.
