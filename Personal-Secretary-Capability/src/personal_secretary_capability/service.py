"""Deterministic Personal Secretary runtime and integration gateways."""
from __future__ import annotations

import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Protocol

from .models import SecretaryRequest, SecretaryResult


class SafetyGateway(Protocol):
    def validate_advice(self, action: str, details: dict[str, Any]) -> bool: ...


class EnhancementGateway(Protocol):
    def insights(self, action: str, payload: dict[str, Any]) -> dict[str, Any]: ...


class AutomationGateway(Protocol):
    def request_execution(self, request: dict[str, Any]) -> dict[str, Any]: ...


class CollaborationGateway(Protocol):
    def collect(self, sources: list[str]) -> dict[str, Any]: ...


class AIHubGateway(Protocol):
    """Reserved optional interface; the v1 runtime never requires it."""
    def recommend(self, context: dict[str, Any]) -> dict[str, Any]: ...


class AllowSafetyGateway:
    def validate_advice(self, action: str, details: dict[str, Any]) -> bool:
        return True


class NullEnhancementGateway:
    def insights(self, action: str, payload: dict[str, Any]) -> dict[str, Any]:
        return {}


class SQLiteExecutionRepository:
    def __init__(self, database_path: str | Path = ":memory:") -> None:
        path = str(database_path)
        if path != ":memory:":
            Path(path).parent.mkdir(parents=True, exist_ok=True)
        self._connection = sqlite3.connect(path)
        self._connection.row_factory = sqlite3.Row
        self._connection.execute(
            "CREATE TABLE IF NOT EXISTS executions (request_id TEXT PRIMARY KEY, action TEXT, "
            "success INTEGER, status TEXT, error_code TEXT, message TEXT, details TEXT, timestamp TEXT)"
        )

    def save(self, result: SecretaryResult) -> None:
        item = result.to_dict()
        with self._connection:
            self._connection.execute(
                "INSERT INTO executions VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                (item["request_id"], item["action"], int(item["success"]), item["status"],
                 item["error_code"], item["message"], json.dumps(item["details"], default=str), item["timestamp"]),
            )

    def count(self) -> int:
        return int(self._connection.execute("SELECT COUNT(*) FROM executions").fetchone()[0])

    def close(self) -> None:
        self._connection.close()


def _items(payload: dict[str, Any], key: str) -> list[dict[str, Any]]:
    value = payload.get(key, [])
    if not isinstance(value, list) or any(not isinstance(item, dict) for item in value):
        raise ValueError(f"{key} must be a list of dictionaries")
    return value


def _priority_score(item: dict[str, Any]) -> float:
    urgency = float(item.get("urgency", 0))
    importance = float(item.get("importance", 0))
    goal = float(item.get("goal_alignment", 0))
    deadline = float(item.get("deadline_pressure", 0))
    return round(urgency * .35 + importance * .35 + goal * .2 + deadline * .1, 3)


class PersonalSecretaryService:
    ACTIONS = frozenset({"daily_briefing", "weekly_review", "monthly_review", "reminder",
                         "recommend", "prioritize", "decision_support", "notify", "secretary"})

    def __init__(self, *, repository: SQLiteExecutionRepository | None = None,
                 safety_gateway: SafetyGateway | None = None,
                 enhancement_gateway: EnhancementGateway | None = None,
                 automation_gateway: AutomationGateway | None = None,
                 collaboration_gateway: CollaborationGateway | None = None,
                 ai_hub_gateway: AIHubGateway | None = None) -> None:
        self.repository = repository or SQLiteExecutionRepository()
        self.safety = safety_gateway or AllowSafetyGateway()
        self.enhancement = enhancement_gateway or NullEnhancementGateway()
        self.automation = automation_gateway
        self.collaboration = collaboration_gateway
        self.ai_hub = ai_hub_gateway
        self._notification_keys: set[str] = set()

    def execute(self, request: SecretaryRequest) -> SecretaryResult:
        if not isinstance(request, SecretaryRequest):
            raise TypeError("request must be a SecretaryRequest")
        context = request.context
        try:
            context.validate()
            if context.action not in self.ACTIONS:
                raise LookupError(f"unsupported action: {context.action}")
            payload = dict(context.payload)
            sources = payload.pop("collaboration_sources", None)
            if sources is not None:
                if self.collaboration is None:
                    raise ValueError("collaboration_sources requires a collaboration gateway")
                if not isinstance(sources, list):
                    raise ValueError("collaboration_sources must be a list")
                payload.update(self.collaboration.collect(sources))
            handler = getattr(self, f"_{context.action}")
            details = handler(payload)
            insights = self.enhancement.insights(context.action, payload)
            if insights:
                details["enhancement_insights"] = insights
            if not self.safety.validate_advice(context.action, details):
                result = SecretaryResult(False, context.request_id, context.action, "BLOCKED",
                                         "Safety validation rejected the advisory output", {}, "SAFETY_REJECTED")
            else:
                execution = payload.get("automation_request")
                if execution is not None:
                    if self.automation is None:
                        raise ValueError("automation_request requires an automation gateway")
                    details["automation_response"] = self.automation.request_execution(execution)
                result = SecretaryResult(True, context.request_id, context.action, "SUCCESS",
                                         "Personal Secretary synthesis completed", details)
        except LookupError as exc:
            result = SecretaryResult(False, context.request_id, context.action, "FAILED", str(exc), {}, "ACTION_NOT_SUPPORTED")
        except (TypeError, ValueError) as exc:
            result = SecretaryResult(False, context.request_id, context.action, "FAILED", str(exc), {}, "INPUT_VALIDATION_FAILED")
        except Exception as exc:
            result = SecretaryResult(False, context.request_id, context.action, "FAILED", f"execution failed: {exc}", {}, "EXECUTION_FAILED")
        self.repository.save(result)
        return result

    def _prioritize(self, payload: dict[str, Any]) -> dict[str, Any]:
        ranked = [{**item, "priority_score": _priority_score(item)} for item in _items(payload, "items")]
        ranked.sort(key=lambda item: (-item["priority_score"], str(item.get("id", item.get("title", "")))))
        return {"ranked_items": ranked, "count": len(ranked)}

    def _reminder(self, payload: dict[str, Any]) -> dict[str, Any]:
        now_value = payload.get("now")
        now = datetime.fromisoformat(now_value.replace("Z", "+00:00")) if isinstance(now_value, str) else datetime.now(timezone.utc)
        if now.tzinfo is None:
            now = now.replace(tzinfo=timezone.utc)
        reminders = []
        for item in _items(payload, "items"):
            due = datetime.fromisoformat(str(item["due_at"]).replace("Z", "+00:00"))
            if due.tzinfo is None:
                due = due.replace(tzinfo=timezone.utc)
            state = "OVERDUE" if due < now else "DUE"
            reminders.append({**item, "state": state, "minutes_until_due": round((due - now).total_seconds() / 60)})
        reminders.sort(key=lambda item: item["due_at"])
        return {"reminders": reminders, "pending_count": len(reminders)}

    def _recommend(self, payload: dict[str, Any]) -> dict[str, Any]:
        candidates = _items(payload, "candidates")
        scored = sorted(({**item, "score": float(item.get("score", 0))} for item in candidates), key=lambda x: (-x["score"], str(x.get("id", ""))))
        return {"recommendations": scored, "recommended": scored[0] if scored else None, "basis": payload.get("current_state", {})}

    def _decision_support(self, payload: dict[str, Any]) -> dict[str, Any]:
        criteria = payload.get("criteria", {})
        if not isinstance(criteria, dict):
            raise ValueError("criteria must be a dictionary")
        compared = []
        for option in _items(payload, "options"):
            values = option.get("values", {})
            score = sum(float(weight) * float(values.get(name, 0)) for name, weight in criteria.items())
            compared.append({**option, "weighted_score": round(score, 3)})
        compared.sort(key=lambda item: (-item["weighted_score"], str(item.get("id", ""))))
        return {"comparison": compared, "recommended": compared[0] if compared else None, "criteria": criteria}

    def _notify(self, payload: dict[str, Any]) -> dict[str, Any]:
        emitted, suppressed = [], []
        for item in _items(payload, "notifications"):
            key = str(item.get("dedupe_key") or item.get("id") or json.dumps(item, sort_keys=True))
            (suppressed if key in self._notification_keys else emitted).append(item)
            self._notification_keys.add(key)
        return {"notifications": emitted, "emitted_count": len(emitted), "suppressed_count": len(suppressed), "status": "ACTIVE" if emitted else "QUIET"}

    def _daily_briefing(self, payload: dict[str, Any]) -> dict[str, Any]:
        tasks = _items(payload, "tasks")
        priorities = self._prioritize({"items": tasks})["ranked_items"]
        return {"period": "daily", "priorities": priorities, "events": _items(payload, "events"),
                "reminders": _items(payload, "reminders"), "recommendations": payload.get("recommendations", []),
                "summary": {"task_count": len(tasks), "event_count": len(payload.get("events", []))}}

    def _review(self, payload: dict[str, Any], period: str) -> dict[str, Any]:
        completed, planned = _items(payload, "completed"), _items(payload, "planned")
        return {"period": period, "summary": {"completed_count": len(completed), "planned_count": len(planned)},
                "completed": completed, "in_progress": _items(payload, "in_progress"),
                "achievements": payload.get("achievements", []), "improvements": payload.get("improvements", []),
                "recommendations": payload.get("recommendations", [])}

    def _weekly_review(self, payload: dict[str, Any]) -> dict[str, Any]:
        return self._review(payload, "weekly")

    def _monthly_review(self, payload: dict[str, Any]) -> dict[str, Any]:
        return self._review(payload, "monthly")

    def _secretary(self, payload: dict[str, Any]) -> dict[str, Any]:
        return {"briefing": self._daily_briefing(payload), "generated_actions": [],
                "advisory_only": True, "ai_required": False}

    def health_check(self) -> dict[str, Any]:
        return {"status": "HEALTHY", "version": "1.0.0", "modules": sorted(self.ACTIONS),
                "ai_required": False, "ai_hub_configured": self.ai_hub is not None}

    def close(self) -> None:
        self.repository.close()

    def __enter__(self) -> "PersonalSecretaryService":
        return self

    def __exit__(self, *_: object) -> None:
        self.close()


def create_default_service(**kwargs: Any) -> PersonalSecretaryService:
    return PersonalSecretaryService(**kwargs)
