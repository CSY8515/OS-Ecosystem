from types import SimpleNamespace

import pytest

from ai_hub.domain.common.errors import ErrorCode, ProviderCallError
from ai_hub.domain.providers import InferenceRequest, Message, ModelRegistration, ProviderFamily
from ai_hub.infrastructure.providers.claude import ClaudeAdapter
from ai_hub.infrastructure.providers.gemini import GeminiAdapter
from ai_hub.infrastructure.providers.openai import OpenAIAdapter


REQUEST = InferenceRequest(
    request_id="req-1",
    caller_id="living-os",
    task_kind="generation",
    messages=(Message("system", "Be concise."), Message("user", "Hello")),
    max_output_tokens=128,
)


def model(family: ProviderFamily) -> ModelRegistration:
    return ModelRegistration(
        model_id=f"{family}-default",
        provider_id=str(family),
        native_name=f"native-{family}",
        task_kinds=frozenset({"generation"}),
    )


class _Create:
    def __init__(self, response=None, error=None):
        self.response, self.error, self.calls = response, error, []
    def create(self, **kwargs):
        self.calls.append(kwargs)
        if self.error: raise self.error
        return self.response
    def generate_content(self, **kwargs):
        return self.create(**kwargs)


def test_openai_adapter_contract() -> None:
    create = _Create(SimpleNamespace(id="o1", output_text="openai", usage=SimpleNamespace(input_tokens=2, output_tokens=3, total_tokens=5)))
    adapter = OpenAIAdapter(lambda credential, timeout: SimpleNamespace(responses=create))
    result = adapter.execute(REQUEST, model(ProviderFamily.OPENAI), "secret", 4)
    assert result.output_text == "openai"
    assert result.usage.total_units == 5
    assert create.calls[0]["store"] is False
    assert create.calls[0]["max_output_tokens"] == 128


def test_gemini_adapter_contract() -> None:
    create = _Create(SimpleNamespace(id="g1", text="gemini", usage_metadata=SimpleNamespace(prompt_token_count=2, candidates_token_count=3, total_token_count=5)))
    adapter = GeminiAdapter(lambda credential, timeout: SimpleNamespace(models=create))
    result = adapter.execute(REQUEST, model(ProviderFamily.GEMINI), "secret", 4)
    assert result.output_text == "gemini"
    assert result.usage.total_units == 5
    assert create.calls[0]["config"]["max_output_tokens"] == 128


def test_claude_adapter_contract() -> None:
    response = SimpleNamespace(id="c1", content=[SimpleNamespace(type="text", text="claude")], usage=SimpleNamespace(input_tokens=2, output_tokens=3))
    create = _Create(response)
    adapter = ClaudeAdapter(lambda credential, timeout: SimpleNamespace(messages=create))
    result = adapter.execute(REQUEST, model(ProviderFamily.CLAUDE), "secret", 4)
    assert result.output_text == "claude"
    assert result.usage.total_units == 5
    assert create.calls[0]["system"] == "Be concise."
    assert create.calls[0]["messages"] == [{"role": "user", "content": "Hello"}]


class AuthenticationError(Exception):
    status_code = 401


@pytest.mark.parametrize(
    "adapter, client",
    [
        (OpenAIAdapter, lambda create: SimpleNamespace(responses=create)),
        (GeminiAdapter, lambda create: SimpleNamespace(models=create)),
        (ClaudeAdapter, lambda create: SimpleNamespace(messages=create)),
    ],
)
def test_adapter_errors_are_sanitized(adapter, client) -> None:
    create = _Create(error=AuthenticationError("secret provider payload"))
    instance = adapter(lambda credential, timeout: client(create))
    family = instance.family
    with pytest.raises(ProviderCallError) as captured:
        instance.execute(REQUEST, model(family), "secret", 4)
    assert captured.value.code == ErrorCode.UNAUTHORIZED
    assert "secret provider payload" not in str(captured.value)


def test_empty_provider_output_is_invalid_response() -> None:
    create = _Create(SimpleNamespace(id="o2", output_text="", usage=None))
    adapter = OpenAIAdapter(lambda credential, timeout: SimpleNamespace(responses=create))
    with pytest.raises(ProviderCallError) as captured:
        adapter.execute(REQUEST, model(ProviderFamily.OPENAI), "secret", 4)
    assert captured.value.code == ErrorCode.INVALID_PROVIDER_RESPONSE


@pytest.mark.parametrize(
    "adapter, client, expected",
    [
        (OpenAIAdapter, SimpleNamespace(models=SimpleNamespace(list=lambda: SimpleNamespace(data=[SimpleNamespace(id="gpt-a")]))), ("gpt-a",)),
        (GeminiAdapter, SimpleNamespace(models=SimpleNamespace(list=lambda: [SimpleNamespace(name="models/gemini-a")])), ("gemini-a",)),
        (ClaudeAdapter, SimpleNamespace(models=SimpleNamespace(list=lambda: SimpleNamespace(data=[SimpleNamespace(id="claude-a")]))), ("claude-a",)),
    ],
)
def test_adapter_model_listing_is_normalized(adapter, client, expected) -> None:
    assert adapter(lambda credential, timeout: client).list_models("secret", 4) == expected


def test_gemini_numeric_error_code_is_retryable() -> None:
    class ClientError(Exception):
        code = 429
    create = _Create(error=ClientError("provider payload"))
    adapter = GeminiAdapter(lambda credential, timeout: SimpleNamespace(models=create))
    with pytest.raises(ProviderCallError) as captured:
        adapter.execute(REQUEST, model(ProviderFamily.GEMINI), "secret", 4)
    assert captured.value.code == ErrorCode.RATE_LIMITED
    assert captured.value.retryable is True
    assert "provider payload" not in str(captured.value)
