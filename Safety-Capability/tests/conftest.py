import pytest
from safety_capability import BasicValidationComponent, ComponentRegistry, SafetyRuntime, SQLiteExecutionRepository

@pytest.fixture
def repository():
    repo = SQLiteExecutionRepository()
    yield repo
    repo.close()

@pytest.fixture
def runtime(repository):
    registry = ComponentRegistry()
    registry.register(BasicValidationComponent())
    return SafetyRuntime(registry=registry, repository=repository)
