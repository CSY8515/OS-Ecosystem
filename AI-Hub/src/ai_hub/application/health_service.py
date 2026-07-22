from __future__ import annotations

from datetime import datetime
from time import monotonic
from typing import Callable

from ai_hub.domain.common.errors import ProviderCallError
from ai_hub.domain.health import HealthObservation, HealthRegistry, HealthState
from ai_hub.domain.providers import InferenceRequest, Message, ModelRegistration, ProviderAdapter, ProviderRegistration


class HealthService:
    def __init__(self, registry: HealthRegistry, timer: Callable[[], float] = monotonic) -> None:
        self._registry = registry
        self._timer = timer

    def check(
        self,
        provider: ProviderRegistration,
        model: ModelRegistration,
        adapter: ProviderAdapter,
        credential: str,
        *,
        checked_at: datetime,
        timeout_seconds: float,
    ) -> HealthObservation:
        if not provider.enabled:
            return self._registry.record(HealthObservation(
                provider.provider_id, HealthState.DISABLED, checked_at, None
            ))
        start = self._timer()
        try:
            adapter.execute(
                InferenceRequest(
                    request_id=f"health-{provider.provider_id}",
                    caller_id="ai-hub-health",
                    task_kind="generation",
                    messages=(Message("user", "Reply OK"),),
                    max_output_tokens=8,
                ),
                model,
                credential,
                timeout_seconds,
            )
            state, error_code = HealthState.ONLINE, None
        except ProviderCallError as error:
            state = HealthState.OFFLINE if error.retryable else HealthState.ERROR
            error_code = str(error.code)
        duration = round(max(0.0, (self._timer() - start) * 1000), 3)
        return self._registry.record(HealthObservation(
            provider.provider_id, state, checked_at, duration, error_code=error_code
        ))
