import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "Automation-Capability" / "src"))
sys.path.insert(0, str(ROOT / "Collaboration-Connectivity-Capability" / "src"))

from automation_capability import AutomationExecutionContext, AutomationRequest, create_default_runtime
from collaboration_connectivity_capability import (
    CollaborationConnectivityService, ConnectionRequest, ConnectorMetadata, ConnectorRegistry,
    ConnectorStatus, ConnectorType, DefaultSafetyGateway, InMemoryConnector,
)


class RecordingSafetyGateway(DefaultSafetyGateway):
    def __init__(self):
        super().__init__()
        self.request_checks = 0
        self.response_checks = 0

    def validate_request(self, request, *, connector_enabled, supported):
        self.request_checks += 1
        return super().validate_request(request, connector_enabled=connector_enabled, supported=supported)

    def validate_response(self, request, response):
        self.response_checks += 1
        return super().validate_response(request, response)


class RecordingEnhancementGateway:
    def __init__(self):
        self.responses = []

    def record_connection_result(self, response):
        self.responses.append(response)


class CrossCapabilityIntegrationTests(unittest.TestCase):
    def test_automation_invokes_safety_governed_connector_and_emits_analysis_data(self):
        registry = ConnectorRegistry()
        registry.register(InMemoryConnector(ConnectorMetadata(
            connector_id="demo", name="Demo", connector_type=ConnectorType.INTERNAL_OS,
            provider="in-memory", version="1.0.0", status=ConnectorStatus.AVAILABLE,
            supported_operations=frozenset({"send"}),
        )))
        safety = RecordingSafetyGateway()
        enhancement = RecordingEnhancementGateway()
        collaboration = CollaborationConnectivityService(registry=registry, safety_gateway=safety, enhancement_gateway=enhancement)
        connector_request = ConnectionRequest("demo", "send", "Automation", "Living OS", {"event": "sync"})
        automation_context = AutomationExecutionContext(
            source="test", target="shared-automation", action="auto_execute",
            payload={"task": {"name": "sync"}, "approval": {"approved": True}, "connector_request": connector_request},
        )

        with create_default_runtime(collaboration_gateway=collaboration) as runtime:
            result = runtime.execute(AutomationRequest(automation_context))

        self.assertTrue(result.success)
        self.assertTrue(result.details["connector_response"]["success"])
        self.assertEqual((safety.request_checks, safety.response_checks), (1, 1))
        self.assertEqual(len(enhancement.responses), 1)
        self.assertEqual(collaboration.recorder.analytics()["success_rate"], 1.0)


if __name__ == "__main__":
    unittest.main()
