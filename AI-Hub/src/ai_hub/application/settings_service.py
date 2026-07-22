from __future__ import annotations

from datetime import datetime
from uuid import uuid4

from ai_hub.domain.settings import HubSettings, SettingsRevision


class SettingsService:
    def __init__(self, repository) -> None:
        self._repository = repository

    def update(self, settings: HubSettings, *, actor_id: str, created_at: datetime) -> SettingsRevision:
        revision = SettingsRevision(f"settings-{uuid4().hex}", created_at, actor_id, settings)
        self._repository.add(revision)
        return revision

    def current(self) -> SettingsRevision | None:
        return self._repository.current()
