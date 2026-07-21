import unittest

from automation_capability import AutomationExecutionContext, AutomationRequest, HealthStatus, StaticEnhancementGateway, create_default_runtime


class RuntimeTests(unittest.TestCase):
    def execute(self, runtime, action, payload, *, metadata=None):
        context = AutomationExecutionContext(source="test-project", target="shared-automation", action=action, payload=payload, metadata=metadata or {})
        return runtime.execute(AutomationRequest(context))

    def test_default_registry_contains_all_core_modules(self):
        with create_default_runtime() as runtime:
            self.assertEqual([item["component_id"] for item in runtime.registry.list_components()], ["auto-decision", "auto-execution", "routine", "scheduler", "trigger", "workflow"])

    def test_workflow(self):
        with create_default_runtime() as runtime:
            result = self.execute(runtime, "manage_workflow", {"steps": [{"name": "validate"}, {"name": "execute", "depends_on": ["validate"]}]})
            self.assertTrue(result.success)
            self.assertEqual(result.details["step_count"], 2)

    def test_scheduler(self):
        with create_default_runtime() as runtime:
            result = self.execute(runtime, "schedule", {"schedule_type": "interval", "interval_minutes": 30})
            self.assertTrue(result.details["recurring"])

    def test_trigger(self):
        with create_default_runtime() as runtime:
            result = self.execute(runtime, "evaluate_trigger", {"condition": {"field": "status", "operator": "equals", "value": "ready"}, "event": {"status": "ready"}})
            self.assertTrue(result.details["matched"])

    def test_routine(self):
        with create_default_runtime() as runtime:
            result = self.execute(runtime, "manage_routine", {"cadence": "weekly", "tasks": ["review"]})
            self.assertEqual(result.details["cadence"], "weekly")

    def test_auto_execution_requires_approval_then_logs_execution(self):
        with create_default_runtime() as runtime:
            pending = self.execute(runtime, "auto_execute", {"task": {"name": "sync"}, "approval": {"approved": False}})
            approved = self.execute(runtime, "auto_execute", {"task": {"name": "sync"}, "approval": {"approved": True}})
            self.assertEqual(pending.status, "PENDING_APPROVAL")
            self.assertTrue(approved.success)
            self.assertEqual(approved.details["status"], "EXECUTED")
            self.assertEqual(runtime.repository.count(), 2)

    def test_auto_decision_consumes_enhancement_insights(self):
        gateway = StaticEnhancementGateway({"patterns": ["morning"], "rule": "prefer-focus"})
        with create_default_runtime(enhancement_gateway=gateway) as runtime:
            result = self.execute(runtime, "auto_decide", {"candidates": [{"id": "a", "score": 0.7}, {"id": "b", "score": 0.9}], "approval_policy": "manual"})
            self.assertEqual(result.details["recommended"]["id"], "b")
            self.assertEqual(result.details["enhancement_inputs"]["rule"], "prefer-focus")
            self.assertTrue(result.details["approval_required"])

    def test_critical_risk_is_blocked_by_safety_gateway(self):
        with create_default_runtime() as runtime:
            result = self.execute(runtime, "manage_routine", {"cadence": "daily", "tasks": ["unsafe"]}, metadata={"risk_level": "CRITICAL"})
            self.assertEqual(result.status, "BLOCKED")
            self.assertEqual(result.error_code, "SAFETY_REJECTED")

    def test_pipeline_and_health(self):
        with create_default_runtime() as runtime:
            result = self.execute(runtime, "manage_workflow", {"steps": [{"name": "run"}]})
            self.assertEqual(result.stages, ("Validation", "Risk Check", "Approval", "Execution", "Logging"))
            health = runtime.health_check()
            self.assertEqual(health["capability"].status, HealthStatus.HEALTHY)
            self.assertEqual(len(health["components"]), 6)

    def test_invalid_input_and_unknown_action_are_recorded(self):
        with create_default_runtime() as runtime:
            self.assertEqual(self.execute(runtime, "schedule", {"schedule_type": "interval", "interval_minutes": 0}).error_code, "INPUT_VALIDATION_FAILED")
            self.assertEqual(self.execute(runtime, "unknown", {}).error_code, "ACTION_NOT_SUPPORTED")
            self.assertEqual(runtime.repository.count(), 2)


if __name__ == "__main__":
    unittest.main()
