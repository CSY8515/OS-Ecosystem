from __future__ import annotations

from collections.abc import Callable

from ai_hub.domain.common.errors import ErrorCode, ProviderCallError
from ai_hub.domain.providers import ProviderFamily, ProviderResult
from ai_hub.infrastructure.providers.shared import attribute, classify_provider_error, close_client
from .mapper import map_input, map_usage


def _default_client_factory(credential: str, timeout_seconds: float):
    from google import genai
    from google.genai import types
    return genai.Client(
        api_key=credential,
        http_options=types.HttpOptions(
            timeout=int(timeout_seconds * 1000),
            retry_options=types.HttpRetryOptions(attempts=1),
        ),
    )


class GeminiAdapter:
    family = ProviderFamily.GEMINI

    def __init__(self, client_factory: Callable = _default_client_factory) -> None:
        self._client_factory = client_factory

    def execute(self, request, model, credential, timeout_seconds) -> ProviderResult:
        client = None
        try:
            client = self._client_factory(credential, timeout_seconds)
            config = {"max_output_tokens": request.max_output_tokens}
            if request.response_format == "json":
                config["response_mime_type"] = "application/json"
            response = client.models.generate_content(
                model=model.native_name,
                contents=map_input(request),
                config=config,
            )
            output = attribute(response, "text", "")
            if not str(output).strip():
                raise ProviderCallError(ErrorCode.INVALID_PROVIDER_RESPONSE, "provider returned no text output")
            return ProviderResult(
                provider=self.family,
                model_id=model.model_id,
                output_text=str(output),
                usage=map_usage(response),
                provider_request_id=attribute(response, "id"),
            )
        except ProviderCallError:
            raise
        except Exception as error:
            raise classify_provider_error(error) from None
        finally:
            if client is not None:
                close_client(client)

    def list_models(self, credential: str, timeout_seconds: float) -> tuple[str, ...]:
        client = None
        try:
            client = self._client_factory(credential, timeout_seconds)
            models = client.models.list()
            names = (attribute(item, "name") for item in models)
            return tuple(sorted(str(name).removeprefix("models/") for name in names if name))
        except Exception as error:
            raise classify_provider_error(error) from None
        finally:
            if client is not None:
                close_client(client)
