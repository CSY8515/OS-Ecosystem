from __future__ import annotations

from typing import Mapping
import os


class SecretUnavailableError(LookupError):
    """Raised without including a secret value or provider payload."""


class EnvironmentSecretResolver:
    def __init__(self, environment: Mapping[str, str] | None = None) -> None:
        self._environment = os.environ if environment is None else environment

    def resolve(self, reference: str) -> str:
        if not reference or not reference.replace("_", "").isalnum():
            raise SecretUnavailableError("invalid secret reference")
        value = self._environment.get(reference)
        if value is None or not value.strip():
            raise SecretUnavailableError(f"secret reference is unavailable: {reference}")
        return value
