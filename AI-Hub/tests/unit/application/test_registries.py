import pytest

from ai_hub.application.api_management_service import APIManagementService
from ai_hub.application.model_registry_service import ModelRegistryService
from ai_hub.application.provider_management_service import ProviderManagementService
from ai_hub.domain.callers import CallerRegistration
from ai_hub.domain.common.errors import AIHubError, ErrorCode
from ai_hub.domain.providers import ModelRegistration, ProviderFamily, ProviderRegistration


def test_provider_and_model_registration_is_explicit() -> None:
    providers = ProviderManagementService()
    provider = ProviderRegistration("openai", ProviderFamily.OPENAI, "OpenAI", "OPENAI_KEY")
    providers.register(provider)
    models = ModelRegistryService()
    model = ModelRegistration("m1", "openai", "native", frozenset({"generation"}))
    models.register(model, provider_exists=True)
    assert providers.list() == (provider,)
    assert models.list("openai") == (model,)
    with pytest.raises(ValueError):
        providers.delete("openai", referenced_by_model=True)


def test_api_management_isolates_caller_scopes() -> None:
    service = APIManagementService()
    service.register(CallerRegistration("living-os", "Living OS", frozenset({"inference"})))
    assert service.authorize("living-os", "inference").caller_id == "living-os"
    with pytest.raises(AIHubError) as captured:
        service.authorize("living-os", "admin")
    assert captured.value.code == ErrorCode.FORBIDDEN
