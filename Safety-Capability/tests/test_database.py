from safety_capability import BasicValidationComponent, ComponentRegistry, SafetyExecutionContext, SafetyRequest, SafetyRuntime, SQLiteExecutionRepository

def test_database_persists_and_can_be_recreated(tmp_path):
    path = tmp_path / "records.db"
    first_repo = SQLiteExecutionRepository(path)
    registry = ComponentRegistry()
    registry.register(BasicValidationComponent())
    runtime = SafetyRuntime(registry=registry, repository=first_repo)
    context = SafetyExecutionContext("database-test", "sqlite", "validate", {"value": True})
    result = runtime.execute(SafetyRequest(context))
    runtime.close()

    second_repo = SQLiteExecutionRepository(path)
    record = second_repo.get(result.request_id)
    assert record is not None
    assert record["success"] is True
    assert record["source"] == "database-test"
    assert record["details"]["valid"] is True
    assert second_repo.count() == 1
    second_repo.close()

def test_database_can_be_created_from_scratch(tmp_path):
    path = tmp_path / "new" / "fresh.db"
    repo = SQLiteExecutionRepository(path)
    assert path.exists()
    assert repo.count() == 0
    repo.close()
