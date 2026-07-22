from __future__ import annotations

from collections import defaultdict, deque
from dataclasses import replace

from .models import HealthObservation, HealthState


class HealthRegistry:
    def __init__(self, window_size: int = 20) -> None:
        if window_size <= 0:
            raise ValueError("window_size must be positive")
        self._history = defaultdict(lambda: deque(maxlen=window_size))

    def record(self, observation: HealthObservation) -> HealthObservation:
        history = self._history[observation.provider_id]
        history.append(observation)
        measured = [item for item in history if item.state not in {HealthState.UNKNOWN, HealthState.DISABLED}]
        availability = None
        if measured:
            availability = sum(item.state == HealthState.ONLINE for item in measured) / len(measured)
        enriched = replace(observation, availability=availability)
        history[-1] = enriched
        return enriched

    def latest(self, provider_id: str) -> HealthObservation | None:
        history = self._history.get(provider_id)
        return history[-1] if history else None

    def all_latest(self) -> tuple[HealthObservation, ...]:
        return tuple(self._history[key][-1] for key in sorted(self._history) if self._history[key])
