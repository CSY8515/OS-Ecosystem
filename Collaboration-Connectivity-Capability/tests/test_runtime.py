import json
import time
import unittest
from dataclasses import replace
from datetime import timedelta

from collaboration_connectivity_capability import (
    CollaborationConnectivityError,
    CollaborationConnectivityService,
    CollaborationMessage,
    ConnectionRequest,
    ConnectorMetadata,
    ConnectorRegistry,
    ConnectorStatus,
    ConnectorType,
    ErrorCode,
    ExportRequest,
    HealthStatus,
    ImportRequest,
    InMemoryConnector,
    InMemoryMessageBus,
    MessageStatus,
    RetryPolicy,
    SyncRequest,
    SyncStatus,
    SynchronizationManager,
    TransformationRule,
    export_data,
    import_data,
    transform_record,
)
from collaboration_connectivity_capability.models import utc_now


def metadata(connector_id="demo", *, operations=None, enabled=True, retry_policy=None):
    return ConnectorMetadata(
        connector_id=connector_id,
        name="Demo Connector",
        connector_type=ConnectorType.INTERNAL_OS,
        provider="in-memory",
        version="1.0.0",
        status=ConnectorStatus.AVAILABLE,
        supported_operations=frozenset(operations or {"connect", "disconnect", "send", "receive", "health_check", "get_status"}),
        enabled=enabled,
        retry_policy=retry_policy or RetryPolicy(),
    )


def request(operation="send", *, connector_id="demo", payload=None, timeout=None, metadata_value=None):
    return ConnectionRequest(connector_id, operation, "Living OS", "Universal Learning Engine", payload, timeout_seconds=timeout, metadata=metadata_value or {})


class ConnectorRegistryTests(unittest.TestCase):
    def test_register_lookup_and_list(self):
        registry = ConnectorRegistry()
        registry.register(InMemoryConnector(metadata("b")))
        registry.register(InMemoryConnector(metadata("a")))
        self.assertEqual([item.connector_id for item in registry.list_connectors()], ["a", "b"])
        self.assertTrue(registry.supports("a", "send"))

    def test_duplicate_registration_is_rejected(self):
        registry = ConnectorRegistry(); registry.register(InMemoryConnector(metadata()))
        with self.assertRaisesRegex(ValueError, "already registered"):
            registry.register(InMemoryConnector(metadata()))

    def test_disable_and_required_lookup(self):
        registry = ConnectorRegistry(); registry.register(InMemoryConnector(metadata()))
        registry.set_enabled("demo", False)
        with self.assertRaises(CollaborationConnectivityError) as raised:
            registry.get("demo", require_enabled=True)
        self.assertEqual(raised.exception.code, ErrorCode.CONNECTOR_DISABLED)


class ServiceTests(unittest.TestCase):
    def create_service(self, connector=None, **kwargs):
        registry = ConnectorRegistry(); registry.register(connector or InMemoryConnector(metadata()))
        return CollaborationConnectivityService(registry=registry, **kwargs)

    def test_normal_request_response_and_execution_record(self):
        service = self.create_service()
        response = service.execute(request(payload={"hello": "world"}))
        self.assertTrue(response.success)
        self.assertEqual(response.data["message_count"], 1)
        record = service.recorder.all()[0]
        self.assertTrue(record.success)
        self.assertEqual(record.operation, "send")

    def test_unsupported_operation_is_standardized(self):
        service = self.create_service()
        response = service.execute(request("export_data"))
        self.assertEqual(response.error_code, "UNSUPPORTED_OPERATION")

    def test_connector_not_found_is_standardized(self):
        service = self.create_service()
        response = service.execute(request(connector_id="missing"))
        self.assertEqual(response.error_code, "CONNECTOR_NOT_FOUND")

    def test_invalid_request_is_standardized(self):
        service = self.create_service()
        response = service.execute(replace(request(), source=""))
        self.assertEqual(response.error_code, "INVALID_REQUEST")

    def test_disabled_connector_is_blocked_by_safety(self):
        service = self.create_service(InMemoryConnector(metadata(enabled=False)))
        response = service.execute(request())
        self.assertEqual(response.error_code, "CONNECTOR_DISABLED")

    def test_critical_external_risk_is_blocked(self):
        service = self.create_service()
        response = service.execute(request(metadata_value={"risk_level": "CRITICAL"}))
        self.assertEqual(response.error_code, "SAFETY_REJECTED")

    def test_timeout_is_standardized(self):
        connector = InMemoryConnector(metadata(operations={"send"}), {"send": lambda _: time.sleep(0.03)})
        response = self.create_service(connector).execute(request(timeout=0.001))
        self.assertEqual(response.error_code, "TIMEOUT")
        self.assertTrue(response.retryable)

    def test_rate_limit_retries_and_records_count(self):
        calls = []
        def limited(_):
            calls.append(1)
            raise CollaborationConnectivityError(ErrorCode.RATE_LIMITED, "limited", retryable=True)
        retry = RetryPolicy(max_attempts=2)
        connector = InMemoryConnector(metadata(operations={"send"}, retry_policy=retry), {"send": limited})
        service = self.create_service(connector)
        response = service.execute(request())
        self.assertEqual(response.error_code, "RATE_LIMITED")
        self.assertEqual(len(calls), 2)
        self.assertEqual(service.recorder.all()[0].retry_count, 1)

    def test_health_check_and_automation_adapter(self):
        service = self.create_service()
        self.assertEqual(service.health_check()["status"], HealthStatus.HEALTHY)
        self.assertTrue(service.execute_connector_request(request("get_status")).success)

    def test_enhancement_gateway_receives_analysis_input(self):
        class Collector:
            def __init__(self): self.responses = []
            def record_connection_result(self, response): self.responses.append(response)
        collector = Collector(); service = self.create_service(enhancement_gateway=collector)
        service.execute(request())
        self.assertEqual(len(collector.responses), 1)
        analytics = service.recorder.analytics()
        self.assertEqual(analytics["success_rate"], 1.0)
        self.assertEqual(analytics["provider_stability"]["demo"], 1.0)
        self.assertEqual(analytics["sync_success_rate"], 0.0)
        self.assertIsNone(collector.responses[0].data)

    def test_sensitive_execution_metadata_is_redacted(self):
        service = self.create_service()
        service.execute(request(metadata_value={"token": "do-not-store", "purpose": "test"}))
        stored = service.recorder.all()[0].metadata
        self.assertEqual(stored["token"], "[REDACTED]")
        self.assertEqual(stored["purpose"], "test")

    def test_unexpected_provider_error_does_not_expose_secret(self):
        connector = InMemoryConnector(metadata(operations={"send"}), {"send": lambda _: (_ for _ in ()).throw(RuntimeError("token=private"))})
        response = self.create_service(connector).execute(request())
        self.assertEqual(response.error_code, "INTERNAL_ERROR")
        self.assertNotIn("private", response.error_message)

    def test_non_request_is_programming_error(self):
        with self.assertRaises(TypeError):
            self.create_service().execute(object())


class ImportExportTransformationTests(unittest.TestCase):
    def test_import_json(self):
        result = import_data(ImportRequest('[{"id": 1}, {"id": 2}]', "json", schema={"id": int}))
        self.assertTrue(result.success)
        self.assertEqual(result.processed_count, 2)

    def test_invalid_json_reports_failure(self):
        result = import_data(ImportRequest("{broken", "JSON"))
        self.assertFalse(result.success)
        self.assertIn("invalid JSON", result.errors[0])

    def test_export_json(self):
        result = export_data(ExportRequest(({"id": 1},), "json"))
        self.assertTrue(result.success)
        self.assertEqual(json.loads(result.content), [{"id": 1}])

    def test_csv_and_jsonl_round_trip_shapes(self):
        csv_result = import_data(ImportRequest("id,name\n1,Ada\n", "csv"))
        jsonl_result = import_data(ImportRequest('{"id":1}\n{"id":2}\n', "jsonl"))
        self.assertEqual(csv_result.records[0]["name"], "Ada")
        self.assertEqual(len(jsonl_result.records), 2)

    def test_field_mapping_and_conversion(self):
        rules = (TransformationRule("rename", "old", "new"), TransformationRule("convert", target="new", target_type="int"), TransformationRule("default", target="enabled", value=True))
        result = transform_record({"old": "7"}, rules)
        self.assertEqual(result.data, {"new": 7, "enabled": True})

    def test_invalid_transformation_is_safe_failure(self):
        result = transform_record({"id": 1}, (TransformationRule("execute-code"),))
        self.assertFalse(result.success)


class MessagingAndSyncTests(unittest.TestCase):
    def test_internal_message_delivery(self):
        bus = InMemoryMessageBus(); message = CollaborationMessage("STATUS", "Living OS", "ULE", {"ready": True})
        sent = bus.send(message)
        self.assertEqual(sent.status, MessageStatus.SENT)
        self.assertEqual(bus.receive("ULE"), (message,))
        self.assertEqual(bus.status(message.message_id), MessageStatus.DELIVERED)

    def test_expired_and_failed_message_statuses(self):
        bus = InMemoryMessageBus(); expired = CollaborationMessage("STATUS", "A", "B", {}, expires_at=utc_now() - timedelta(seconds=1))
        self.assertEqual(bus.send(expired).status, MessageStatus.EXPIRED)
        current = CollaborationMessage("STATUS", "A", "B", {})
        bus.send(current)
        self.assertEqual(bus.mark_failed(current.message_id).status, MessageStatus.FAILED)

    def test_sync_create_start_complete(self):
        manager = SynchronizationManager(); record = manager.create(SyncRequest("demo", "A", "B", (1, 2)))
        self.assertEqual(record.status, SyncStatus.PENDING)
        self.assertEqual(manager.start(record.sync_id).status, SyncStatus.RUNNING)
        completed = manager.complete(record.sync_id, processed_count=2, success_count=2)
        self.assertEqual(completed.status, SyncStatus.COMPLETED)

    def test_sync_partial_failure(self):
        manager = SynchronizationManager(); record = manager.create(SyncRequest("demo", "A", "B"))
        partial = manager.complete(record.sync_id, processed_count=3, success_count=2, failure_count=1)
        self.assertEqual(partial.status, SyncStatus.PARTIAL)


if __name__ == "__main__":
    unittest.main()
