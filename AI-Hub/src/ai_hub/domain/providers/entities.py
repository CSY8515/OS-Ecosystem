from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class ProviderFamily(StrEnum):
    OPENAI = "openai"
    GEMINI = "gemini"
    CLAUDE = "claude"


@dataclass(frozen=True, slots=True)
class ProviderRegistration:
    provider_id: str
    family: ProviderFamily
    display_name: str
    secret_reference: str
    enabled: bool = True

    def __post_init__(self) -> None:
        if not self.provider_id.strip() or not self.display_name.strip():
            raise ValueError("provider identity is required")
        if not self.secret_reference.strip():
            raise ValueError("secret_reference is required")


@dataclass(frozen=True, slots=True)
class ModelRegistration:
    model_id: str
    provider_id: str
    native_name: str
    task_kinds: frozenset[str]
    enabled: bool = True
    routing_priority: int = 100
    suitability: float = 0.5
    max_output_tokens: int | None = None

    def __post_init__(self) -> None:
        if not self.model_id.strip() or not self.provider_id.strip() or not self.native_name.strip():
            raise ValueError("model identity is required")
        if not 0 <= self.suitability <= 1:
            raise ValueError("suitability must be between zero and one")
        if self.max_output_tokens is not None and self.max_output_tokens <= 0:
            raise ValueError("max_output_tokens must be positive")
