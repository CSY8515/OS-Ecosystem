from __future__ import annotations

from collections.abc import Mapping
from typing import Any
import re


_SENSITIVE_KEYS = {"api_key", "apikey", "authorization", "secret", "token", "password"}
_BEARER_PATTERN = re.compile(r"(?i)bearer\s+[a-z0-9._~+/-]+")


def sanitize_text(value: object, *, maximum_length: int = 240) -> str:
    text = _BEARER_PATTERN.sub("Bearer [REDACTED]", str(value))
    text = text.replace("\r", " ").replace("\n", " ").strip()
    return text[:maximum_length]


def redact_mapping(values: Mapping[str, Any]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in values.items():
        if key.lower() in _SENSITIVE_KEYS or any(part in key.lower() for part in _SENSITIVE_KEYS):
            result[key] = "[REDACTED]"
        elif isinstance(value, Mapping):
            result[key] = redact_mapping(value)
        else:
            result[key] = value
    return result
