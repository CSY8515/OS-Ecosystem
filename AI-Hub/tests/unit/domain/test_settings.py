import pytest

from ai_hub.domain.settings import HubSettings


def test_default_settings_match_approved_policy() -> None:
    settings = HubSettings()
    policy = settings.to_routing_policy("settings-1")
    assert policy.version == "settings-1"
    assert policy.retry_count == 2
    assert policy.health_weight == 0.30


@pytest.mark.parametrize(
    "values",
    [
        {"auto_routing": False},
        {"retry_count": -1},
        {"timeout_seconds": 0},
        {"timeout_seconds": 10, "overall_timeout_seconds": 5},
        {"health_weight": 0.5},
        {"health_check_interval_seconds": 0},
    ],
)
def test_invalid_settings_are_rejected(values) -> None:
    with pytest.raises(ValueError):
        HubSettings(**values)
