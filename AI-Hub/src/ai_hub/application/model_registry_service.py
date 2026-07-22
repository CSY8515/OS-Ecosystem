from ai_hub.domain.providers import ModelRegistration


class ModelRegistryService:
    def __init__(self) -> None:
        self._models: dict[str, ModelRegistration] = {}

    def register(self, model: ModelRegistration, *, provider_exists: bool) -> None:
        if not provider_exists:
            raise ValueError("model provider is not registered")
        if model.model_id in self._models:
            raise ValueError("model is already registered")
        self._models[model.model_id] = model

    def list(self, provider_id: str | None = None) -> tuple[ModelRegistration, ...]:
        values = self._models.values()
        if provider_id is not None:
            values = (item for item in values if item.provider_id == provider_id)
        return tuple(sorted(values, key=lambda item: item.model_id))
