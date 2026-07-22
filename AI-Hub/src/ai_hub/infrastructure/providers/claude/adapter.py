from __future__ import annotations

from collections.abc import Callable

from ai_hub.domain.common.errors import ErrorCode, ProviderCallError
from ai_hub.domain.providers import ProviderFamily, ProviderResult
from ai_hub.infrastructure.providers.shared import attribute, classify_provider_error, close_client
from .mapper import map_messages, map_output, map_usage


def _default_client_factory(credential: str, timeout_seconds: float):
    from anthropic import Anthropic
    return Anthropic(api_key=credential, timeout=timeout_seconds, max_retries=0)


class ClaudeAdapter:
    family = ProviderFamily.CLAUDE

    def __init__(self, client_factory: Callable = _default_client_factory) -> None:
        self._client_factory = client_factory

    def execute(self, request, model, credential, timeout_seconds) -> ProviderResult:
        client = None
        try:
            client = self._client_factory(credential, timeout_seconds)
            system, messages = map_messages(request)
            arguments = {
                "model": model.native_name,
                "max_tokens": request.max_output_tokens,
                "messages": messages,
            }
            if system:
                arguments["system"] = system
            response = client.messages.create(**arguments)
            output = map_output(response)
            if not output.strip():
                raise ProviderCallError(ErrorCode.INVALID_PROVIDER_RESPONSE, "provider returned no text output")
            return ProviderResult(
                provider=self.family,
                model_id=model.model_id,
                output_text=output,
                usage=map_usage(response),
                provider_request_id=attribute(response, "id") or attribute(response, "_request_id"),
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
