# Automation Capability v1.0

Automation Capability is the OS Ecosystem's independent shared platform for Workflow, Scheduler, Trigger, Routine, Auto Execution, and Auto Decision. Living OS, Universal Learning Engine, and future projects use one project-neutral request/result contract.

The package mirrors the established Safety and Enhancement boundaries: `core`, `interfaces`, `registry`, `execution`, `database`, `components`, `tests`, and `docs`.

```python
from automation_capability import AutomationExecutionContext, AutomationRequest, create_default_runtime

with create_default_runtime() as runtime:
    context = AutomationExecutionContext(
        source="living-os", target="daily-review", action="manage_routine",
        payload={"cadence": "daily", "tasks": ["review", "plan"]},
    )
    result = runtime.execute(AutomationRequest(context))
```

Auto Execution uses an explicit Safety gateway and requires approval. Auto Decision can consume approved Analytics, Pattern Analysis, Optimization, and Rule Generation results through the Enhancement gateway. The default implementation performs no external side effects; host projects retain execution authority.

Run tests with `python -m pytest` from this directory.

