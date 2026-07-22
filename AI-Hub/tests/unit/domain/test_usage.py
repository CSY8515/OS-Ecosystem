from datetime import UTC, datetime

from ai_hub.domain.executions import ExecutionSummary
from ai_hub.domain.predictions import PredictionConfidence, predict_usage_limit
from ai_hub.domain.usage import build_usage_analytics


NOW = datetime(2026, 7, 22, tzinfo=UTC)


def record(identity: str, success: bool, units=None):
    return ExecutionSummary(identity, identity, "ule", NOW, "generation", 10, success, 1, "v0.1",
                            provider_id="openai" if success else None, model_id="m1" if success else None,
                            error_code=None if success else "timeout", total_units=units)


def test_usage_analytics_preserves_unknown_usage() -> None:
    analytics = build_usage_analytics([record("1", True, 5), record("2", False)])
    assert analytics.call_count == 2
    assert analytics.success_rate == 0.5
    assert analytics.total_usage_units == 5
    assert analytics.by_provider == (("openai", 1),)
    assert build_usage_analytics([]).total_usage_units is None


def test_prediction_is_deterministic_and_confidence_labeled() -> None:
    prediction = predict_usage_limit(generated_at=NOW, allowance_units=1000, consumed_units=200,
                                     evidence_days=10, evidence_count=20)
    assert prediction.remaining_units == 800
    assert prediction.daily_usage_units == 20
    assert prediction.estimated_days_remaining == 40
    assert prediction.confidence == PredictionConfidence.MEDIUM


def test_prediction_reports_insufficient_evidence() -> None:
    prediction = predict_usage_limit(generated_at=NOW, allowance_units=None, consumed_units=None,
                                     evidence_days=0, evidence_count=0)
    assert prediction.confidence == PredictionConfidence.INSUFFICIENT
    assert prediction.estimated_days_remaining is None
