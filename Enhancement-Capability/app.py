"""Executable Enhancement Capability v1.0 demonstration."""
from pathlib import Path
from enhancement_capability import EnhancementExecutionContext, EnhancementRequest, SQLiteExecutionRepository, create_default_runtime

def main() -> None:
    repository = SQLiteExecutionRepository(Path(__file__).parent / "data" / "enhancement_executions.db")
    with create_default_runtime(repository=repository) as runtime:
        context = EnhancementExecutionContext(source="example", target="demo", action="analyze", payload={"values": [2, 4, 6]})
        result = runtime.execute(EnhancementRequest(context))
        print("Result:", result.to_dict())
        print("Registered modules:", runtime.registry.list_components())
        print("Health:", runtime.health_check())

if __name__ == "__main__":
    main()
