# AI Hub v0.1 Provider Adapter Contract

Status: Implemented candidate

Every adapter implements the `ProviderAdapter` port and must:

- accept a neutral request, registered model, short-lived credential, and timeout
- return only normalized text, usage, model identity, and safe request metadata
- enforce the supplied timeout through its client
- disable hidden SDK retries where the SDK exposes that control
- classify errors into stable AI Hub categories without provider payload text
- reject empty text output
- expose no SDK object outside the adapter

The Router selects candidates; adapters never select, retry, or fail over to another provider. OpenAI uses Responses, Gemini uses Generate Content with SDK retries fixed to one total attempt, and Claude uses Messages. Every adapter also exposes sanitized model identifiers through `list_models`. New providers must pass the shared adapter contract tests.
