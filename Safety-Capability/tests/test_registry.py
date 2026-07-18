import pytest
from safety_capability import BasicValidationComponent, ComponentRegistry

def test_register_get_list_and_action_lookup():
    registry = ComponentRegistry()
    component = BasicValidationComponent()
    registry.register(component)
    assert registry.get(component.component_id) is component
    assert registry.find_for_action("validate") is component
    assert registry.list_components()[0]["version"] == "1.0.0"

def test_duplicate_registration_is_blocked():
    registry = ComponentRegistry()
    registry.register(BasicValidationComponent())
    with pytest.raises(ValueError, match="already registered"):
        registry.register(BasicValidationComponent())

def test_disabled_component_is_not_selected():
    registry = ComponentRegistry()
    registry.register(BasicValidationComponent())
    registry.set_enabled("basic-validation", False)
    assert registry.is_enabled("basic-validation") is False
    with pytest.raises(Exception) as caught:
        registry.find_for_action("validate")
    assert caught.value.code.value == "ACTION_NOT_SUPPORTED"
