from __future__ import annotations

from collections.abc import Callable

from ai_hub.domain.common.errors import ErrorCode, ProviderCallError
from ai_hub.domain.providers import InferenceRequest, ModelRegistration, ProviderFamily, ProviderResult
from ai_hub.infrastructure.providers.shared import attribute, classify_provider_error, close_client
from .mapper import map_input, map_usage


def _default_client_factory(credential: str, timeout_seconds: float):
    from openai import OpenAI
    return OpenAI(api_key=credential, timeout=timeout_seconds, max_retries=0)


class OpenAIAdapter:
    family = ProviderFamily.OPENAI

    def __init__(self, client_factory: Callable = _default_client_factory) -> None:
        self._client_factory = client_factory

    def execute(self, request, model, credential, timeout_seconds) -> ProviderResult:
        client = None
        try:
            client = self._client_factory(credential, timeout_seconds)
            response = client.responses.create(
                model=model.native_name,
                input=map_input(request),
                max_output_tokens=request.max_output_tokens,
                store=False,
            )
            output = attribute(response, "output_text", "")
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
            page = client.models.list()
            return tuple(sorted(str(attribute(item, "id")) for item in attribute(page, "data", ()) if attribute(item, "id")))
        except Exception as error:
            raise classify_provider_error(error) from None
        finally:
            if client is not None:
                close_client(client)
