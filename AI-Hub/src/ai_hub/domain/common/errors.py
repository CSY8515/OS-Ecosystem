from __future__ import annotations

from enum import StrEnum


class ErrorCode(StrEnum):
    INVALID_REQUEST = "invalid_request"
    UNAUTHORIZED = "unauthorized"
    FORBIDDEN = "forbidden"
    NO_ELIGIBLE_PROVIDER = "no_eligible_provider"
    CREDENTIAL_UNAVAILABLE = "credential_unavailable"
    TIMEOUT = "timeout"
    RATE_LIMITED = "rate_limited"
    PROVIDER_UNAVAILABLE = "provider_unavailable"
    PROVIDER_ERROR = "provider_error"
    INVALID_PROVIDER_RESPONSE = "invalid_provider_response"
    USAGE_LIMIT_REACHED = "usage_limit_reached"
    INTERNAL_ERROR = "internal_error"


class AIHubError(Exception):
    def __init__(self, code: ErrorCode, safe_message: str, *, retryable: bool = False) -> None:
        super().__init__(safe_message)
        self.code = code
        self.safe_message = safe_message
        self.retryable = retryable


class ProviderCallError(AIHubError):
    pass
