# Error Code Reference

Version: v1.0.0

| Code | Meaning | Normally retryable |
| --- | --- | --- |
| `CONNECTOR_NOT_FOUND` | No registered connector matches the request | No |
| `CONNECTOR_DISABLED` | The connector is administratively disabled | No |
| `CONNECTION_FAILED` | Provider connection could not be established | Provider-defined |
| `AUTHENTICATION_FAILED` | Authentication was rejected | No |
| `AUTHORIZATION_FAILED` | The action is not permitted | No |
| `TIMEOUT` | The bounded execution window elapsed | Yes |
| `RATE_LIMITED` | Provider capacity policy rejected the request | Yes |
| `INVALID_REQUEST` | The request contract is invalid | No |
| `INVALID_RESPONSE` | Response identity or shape is invalid | No |
| `UNSUPPORTED_OPERATION` | The connector does not declare the operation | No |
| `IMPORT_FAILED` | Import parsing or validation failed | No |
| `EXPORT_FAILED` | Export validation or encoding failed | No |
| `TRANSFORMATION_FAILED` | A mechanical mapping failed | No |
| `SYNC_FAILED` | Synchronization lifecycle failed | Context-dependent |
| `EXTERNAL_SERVICE_UNAVAILABLE` | Provider is unavailable | Yes |
| `SAFETY_REJECTED` | Safety policy blocked execution | No |
| `INTERNAL_ERROR` | An unexpected failure was isolated | No |

Only errors listed in connector `RetryPolicy.retryable_errors` may be retried, and attempts are always bounded.
