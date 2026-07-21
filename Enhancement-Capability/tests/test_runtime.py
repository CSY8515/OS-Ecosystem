import unittest
from enhancement_capability import EnhancementExecutionContext, EnhancementRequest, HealthStatus, create_default_runtime

class RuntimeTests(unittest.TestCase):
    def execute(self, runtime, action, payload):
        context = EnhancementExecutionContext(source="test-project", target="shared-enhancement", action=action, payload=payload)
        return runtime.execute(EnhancementRequest(context))

    def test_default_registry_contains_all_core_modules(self):
        with create_default_runtime() as runtime:
            self.assertEqual([item["component_id"] for item in runtime.registry.list_components()], ["analytics", "knowledge-management", "learning", "optimization", "pattern-analysis", "rule-generation"])

    def test_each_core_module_executes_and_records(self):
        cases = [("analyze", {"values": [1, 2, 3]}, "analytics"), ("learn", {"examples": [{"topic": "systems"}]}, "learning"), ("analyze_patterns", {"items": ["a", "a", "b"]}, "pattern-analysis"), ("manage_knowledge", {"entries": {"b": 2, "a": 1}}, "knowledge-management"), ("optimize", {"candidates": [{"id": "a", "score": 1}, {"id": "b", "score": 2}]}, "optimization"), ("generate_rules", {"patterns": ["repeat", "repeat", "new"]}, "rule-generation")]
        with create_default_runtime() as runtime:
            for action, payload, component in cases:
                result = self.execute(runtime, action, payload)
                self.assertTrue(result.success)
                self.assertEqual(result.component_id, component)
                self.assertTrue(runtime.repository.get(result.request_id)["success"])

    def test_invalid_input_is_isolated_and_recorded(self):
        with create_default_runtime() as runtime:
            result = self.execute(runtime, "analyze", {"values": []})
            self.assertFalse(result.success)
            self.assertEqual(result.error_code, "INPUT_VALIDATION_FAILED")
            self.assertEqual(runtime.repository.count(), 1)

    def test_unknown_action_and_health(self):
        with create_default_runtime() as runtime:
            self.assertEqual(self.execute(runtime, "unknown", {}).error_code, "ACTION_NOT_SUPPORTED")
            report = runtime.health_check()
            self.assertEqual(report["capability"].status, HealthStatus.HEALTHY)
            self.assertEqual(len(report["components"]), 6)

    def test_non_request_is_a_programming_error(self):
        with create_default_runtime() as runtime, self.assertRaises(TypeError):
            runtime.execute(object())

if __name__ == "__main__":
    unittest.main()
