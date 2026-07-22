# AI Hub v0.1 Routing Policy

Status: Implemented candidate

## Eligibility order

Provider enabled, model enabled, credential available, caller allowed, acceptable Health, supported task, output limit, remaining usage, and Default Provider constraint when Auto Routing is disabled.

## Score

| Evidence | Weight |
| --- | ---: |
| Health and availability | 30% |
| Task suitability | 25% |
| Remaining usage | 20% |
| Latency | 15% |
| Reliability | 10% |

Unknown evidence receives a conservative 0.5 score only after the candidate passes policy. Unknown Health is excluded by default. Equal scores use routing priority and stable model ID. The attempt plan contains at most `1 + retry_count` unique candidates.

Failover continues only after a retryable classified failure. Authentication, permission, invalid request, and invalid structured output terminate the request.
