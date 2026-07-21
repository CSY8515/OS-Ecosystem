from personal_secretary_capability import SecretaryContext, SecretaryRequest, create_default_service


def run(service, action, payload):
    return service.execute(SecretaryRequest(SecretaryContext(source="test", action=action, payload=payload)))


def test_all_core_functions_and_health():
    with create_default_service() as service:
        daily = run(service, "daily_briefing", {"tasks": [{"id": "focus", "urgency": 5, "importance": 5}], "events": [], "reminders": []})
        weekly = run(service, "weekly_review", {"completed": [{"id": "a"}], "planned": [], "in_progress": []})
        monthly = run(service, "monthly_review", {"completed": [], "planned": [{"id": "b"}], "in_progress": []})
        reminder = run(service, "reminder", {"now": "2026-07-21T12:00:00+00:00", "items": [{"id": "x", "due_at": "2026-07-21T11:00:00+00:00"}]})
        recommendation = run(service, "recommend", {"current_state": {"energy": "high"}, "candidates": [{"id": "a", "score": .4}, {"id": "b", "score": .9}]})
        priority = run(service, "prioritize", {"items": [{"id": "a", "urgency": 1}, {"id": "b", "urgency": 5}]})
        decision = run(service, "decision_support", {"criteria": {"value": .7, "cost": -.3}, "options": [{"id": "a", "values": {"value": 4, "cost": 1}}, {"id": "b", "values": {"value": 3, "cost": 4}}]})
        notice = run(service, "notify", {"notifications": [{"id": "n1", "message": "Due"}]})
        secretary = run(service, "secretary", {"tasks": [], "events": [], "reminders": []})
        assert all(item.success for item in (daily, weekly, monthly, reminder, recommendation, priority, decision, notice, secretary))
        assert reminder.details["reminders"][0]["state"] == "OVERDUE"
        assert recommendation.details["recommended"]["id"] == "b"
        assert priority.details["ranked_items"][0]["id"] == "b"
        assert decision.details["recommended"]["id"] == "a"
        assert secretary.details["advisory_only"] is True
        assert service.repository.count() == 9
        assert service.health_check()["ai_required"] is False


def test_notification_deduplication():
    with create_default_service() as service:
        first = run(service, "notify", {"notifications": [{"dedupe_key": "same"}]})
        second = run(service, "notify", {"notifications": [{"dedupe_key": "same"}]})
        assert first.details["emitted_count"] == 1
        assert second.details["suppressed_count"] == 1


def test_integrations_are_explicit_and_safety_can_block():
    class Safety:
        def validate_advice(self, action, details): return False
    class Enhancement:
        def insights(self, action, payload): return {"pattern": "morning"}
    with create_default_service(safety_gateway=Safety(), enhancement_gateway=Enhancement()) as service:
        result = run(service, "recommend", {"candidates": [{"id": "a", "score": 1}]})
        assert result.status == "BLOCKED"
        assert result.error_code == "SAFETY_REJECTED"


def test_collaboration_collection_and_automation_handoff():
    class Collaboration:
        def collect(self, sources):
            assert sources == ["living-os"]
            return {"tasks": [{"id": "shared", "importance": 5}], "events": [], "reminders": []}
    class Automation:
        def request_execution(self, request):
            return {"accepted": True, "request": request}
    with create_default_service(collaboration_gateway=Collaboration(), automation_gateway=Automation()) as service:
        result = run(service, "daily_briefing", {"collaboration_sources": ["living-os"], "automation_request": {"action": "schedule_review"}})
        assert result.success
        assert result.details["priorities"][0]["id"] == "shared"
        assert result.details["automation_response"]["accepted"] is True


def test_invalid_requests_are_recorded():
    with create_default_service() as service:
        assert run(service, "unknown", {}).error_code == "ACTION_NOT_SUPPORTED"
        assert run(service, "prioritize", {"items": "bad"}).error_code == "INPUT_VALIDATION_FAILED"
        assert service.repository.count() == 2
