"""Executable Automation Capability v1.0 demonstration."""

from automation_capability import AutomationExecutionContext, AutomationRequest, create_default_runtime


if __name__ == "__main__":
    with create_default_runtime() as runtime:
        context = AutomationExecutionContext(source="example", target="daily-review", action="manage_routine", payload={"cadence": "daily", "tasks": ["review inbox", "plan next actions"]})
        print(runtime.execute(AutomationRequest(context)).to_dict())
