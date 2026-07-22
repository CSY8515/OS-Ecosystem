from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol, runtime_checkable

from .entities import ModelRegistration, ProviderFamily


ALLOWED_TASK_KINDS = frozenset({
    "generation", "reasoning", "summarization", "extraction", "classification", "structured_generation"
})


@dataclass(frozen=True, slots=True)
class Message:
    role: str
    content: str

    def __post_init__(self) -> None:
        if self.role not in {"system", "developer", "user", "assistant"}:
            raise ValueError("unsupported message role")
        if not self.content.strip():
            raise ValueError("message content is required")


@dataclass(frozen=True, slots=True)
class InferenceRequest:
    request_id: str
    caller_id: str
    task_kind: str
    messages: tuple[Message, ...]
    max_output_tokens: int = 1024
    response_format: str = "text"

    def __post_init__(self) -> None:
        if not self.request_id.strip() or not self.caller_id.strip():
            raise ValueError("request and caller identity are required")
        if self.task_kind not in ALLOWED_TASK_KINDS:
            raise ValueError("unsupported task kind")
        if not self.messages:
            raise ValueError("at least one message is required")
        if self.max_output_tokens <= 0:
            raise ValueError("max_output_tokens must be positive")
        if self.response_format not in {"text", "json"}:
            raise ValueError("response_format must be text or json")


@dataclass(frozen=True, slots=True)
class Usage:
    input_units: int | None = None
    output_units: int | None = None
    total_units: int | None = None
    source: str = "provider"


@dataclass(frozen=True, slots=True)
class ProviderResult:
    provider: ProviderFamily
    model_id: str
    output_text: str
    usage: Usage = Usage()
    provider_request_id: str | None = None

    def __post_init__(self) -> None:
        if not self.output_text.strip():
            raise ValueError("provider returned no text output")


@runtime_checkable
class ProviderAdapter(Protocol):
    family: ProviderFamily

    def execute(
        self,
        request: InferenceRequest,
        model: ModelRegistration,
        credential: str,
        timeout_seconds: float,
    ) -> ProviderResult: ...

    def list_models(self, credential: str, timeout_seconds: float) -> tuple[str, ...]: ...
