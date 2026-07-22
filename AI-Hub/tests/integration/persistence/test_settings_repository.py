from datetime import UTC, datetime, timedelta
from pathlib import Path

import pytest

from ai_hub.application.settings_service import SettingsService
from ai_hub.domain.settings import HubSettings
from ai_hub.infrastructure.persistence import SQLiteSettingsRepository


def test_settings_are_versioned_and_immutable(tmp_path: Path) -> None:
    repository = SQLiteSettingsRepository(tmp_path / "hub.sqlite3")
    repository.migrate()
    service = SettingsService(repository)
    now = datetime(2026, 7, 22, tzinfo=UTC)
    first = service.update(HubSettings(), actor_id="operator", created_at=now)
    second = service.update(HubSettings(retry_count=1), actor_id="operator", created_at=now + timedelta(seconds=1))
    assert service.current() == second
    assert repository.history() == (first, second)
    assert first.settings.retry_count == 2


def test_settings_repository_requires_explicit_migration(tmp_path: Path) -> None:
    repository = SQLiteSettingsRepository(tmp_path / "hub.sqlite3")
    with pytest.raises(Exception):
        SettingsService(repository).update(
            HubSettings(), actor_id="operator", created_at=datetime(2026, 7, 22, tzinfo=UTC)
        )
