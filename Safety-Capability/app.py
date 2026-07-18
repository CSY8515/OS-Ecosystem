"""Minimal executable demonstration for Safety Capability v1.0."""
from pathlib import Path
from safety_capability import (BasicValidationComponent, SafetyExecutionContext,
                               SafetyRequest, SafetyRuntime, SQLiteExecutionRepository)

def main() -> None:
    database = Path(__file__).parent / "data" / "safety_executions.db"
    repository = SQLiteExecutionRepository(database)
    with SafetyRuntime(repository=repository) as runtime:
        runtime.registry.register(BasicValidationComponent())
        context = SafetyExecutionContext(source="example", target="demo",
                                         action="validate", payload={"value": "ready"})
        result = runtime.execute(SafetyRequest(context))
        print("Result:", result.to_dict())
        print("Stored record:", repository.get(context.request_id))
        print("Health:", runtime.health_check())

if __name__ == "__main__":
    main()
