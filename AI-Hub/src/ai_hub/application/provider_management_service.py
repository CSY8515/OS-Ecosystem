from dataclasses import replace

from ai_hub.domain.providers import ProviderRegistration


class ProviderManagementService:
    def __init__(self) -> None:
        self._providers: dict[str, ProviderRegistration] = {}

    def register(self, provider: ProviderRegistration) -> None:
        if provider.provider_id in self._providers:
            raise ValueError("provider is already registered")
        self._providers[provider.provider_id] = provider

    def set_enabled(self, provider_id: str, enabled: bool) -> ProviderRegistration:
        provider = replace(self.get(provider_id), enabled=enabled)
        self._providers[provider_id] = provider
        return provider

    def delete(self, provider_id: str, *, referenced_by_model: bool = False) -> None:
        if referenced_by_model:
            raise ValueError("provider is referenced by a model")
        self._providers.pop(provider_id)

    def get(self, provider_id: str) -> ProviderRegistration:
        try:
            return self._providers[provider_id]
        except KeyError:
            raise LookupError("provider is not registered") from None

    def list(self) -> tuple[ProviderRegistration, ...]:
        return tuple(self._providers[key] for key in sorted(self._providers))
