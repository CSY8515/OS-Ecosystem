from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum


class PredictionConfidence(StrEnum):
    INSUFFICIENT = "Insufficient"
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"


@dataclass(frozen=True, slots=True)
class UsagePrediction:
    generated_at: datetime
    method_version: str
    evidence_count: int
    remaining_units: int | None
    daily_usage_units: float | None
    estimated_days_remaining: float | None
    confidence: PredictionConfidence
    assumptions: tuple[str, ...]


def predict_usage_limit(
    *, generated_at: datetime, allowance_units: int | None, consumed_units: int | None,
    evidence_days: int, evidence_count: int,
) -> UsagePrediction:
    if allowance_units is None or consumed_units is None or evidence_days <= 0 or evidence_count <= 0:
        return UsagePrediction(generated_at, "v0.1-linear", evidence_count, None, None, None,
                               PredictionConfidence.INSUFFICIENT, ("allowance or usage evidence unavailable",))
    remaining = max(0, allowance_units - consumed_units)
    daily = consumed_units / evidence_days
    days = remaining / daily if daily > 0 else None
    confidence = PredictionConfidence.HIGH if evidence_count >= 30 and evidence_days >= 14 else (
        PredictionConfidence.MEDIUM if evidence_count >= 10 and evidence_days >= 7 else PredictionConfidence.LOW
    )
    return UsagePrediction(generated_at, "v0.1-linear", evidence_count, remaining, daily, days, confidence,
                           ("future consumption follows the observed daily average",))
