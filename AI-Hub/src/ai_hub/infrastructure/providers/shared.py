from __future__ import annotations

from typing import Any

from ai_hub.domain.common.errors import ErrorCode, ProviderCallError


def attribute(value: Any, name: str, default=None):
    if isinstance(value, dict):
        return value.get(name, default)
    return getattr(value, name, default)


def close_client(client: Any) -> None:
    close = getattr(client, "close", None)
    if callable(close):
        close()


def classify_provider_error(error: Exception) -> ProviderCallError:
    name = type(error).__name__.lower()
    status = getattr(error, "status_code", None)
    if status is None:
        status = getattr(error, "code", None)
    if status in {401} or "authentication" in name:
        return ProviderCallError(ErrorCode.UNAUTHORIZED, "provider authentication failed")
    if status in {403} or "permission" in name:
        return ProviderCallError(ErrorCode.FORBIDDEN, "provider permission denied")
    if status == 429 or "ratelimit" in name or "rate_limit" in name:
        return ProviderCallError(ErrorCode.RATE_LIMITED, "provider rate limit reached", retryable=True)
    if status in {408, 409} or "timeout" in name:
        return ProviderCallError(ErrorCode.TIMEOUT, "provider request timed out", retryable=True)
    if (isinstance(status, int) and status >= 500) or "connection" in name:
        return ProviderCallError(ErrorCode.PROVIDER_UNAVAILABLE, "provider is temporarily unavailable", retryable=True)
    if status in {400, 404, 422}:
        return ProviderCallError(ErrorCode.PROVIDER_ERROR, "provider rejected the request")
    return ProviderCallError(ErrorCode.PROVIDER_ERROR, "provider request failed")
