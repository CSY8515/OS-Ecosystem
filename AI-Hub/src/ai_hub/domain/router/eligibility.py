from ai_hub.domain.health import HealthState
from ai_hub.domain.providers import InferenceRequest
from .models import RoutingCandidate
from .policy import RoutingPolicy


def exclusion_reason(candidate: RoutingCandidate, request: InferenceRequest, policy: RoutingPolicy) -> str | None:
    if not candidate.provider.enabled:
        return "provider_disabled"
    if not candidate.model.enabled:
        return "model_disabled"
    if not candidate.credential_available:
        return "credential_unavailable"
    if not candidate.caller_allowed:
        return "caller_policy_denied"
    state = candidate.health.state if candidate.health else HealthState.UNKNOWN
    if state in {HealthState.OFFLINE, HealthState.ERROR, HealthState.DISABLED}:
        return f"health_{state.value.lower()}"
    if state == HealthState.UNKNOWN and not policy.allow_unknown_health:
        return "health_unknown"
    if request.task_kind not in candidate.model.task_kinds:
        return "task_unsupported"
    if candidate.model.max_output_tokens is not None and request.max_output_tokens > candidate.model.max_output_tokens:
        return "output_limit_exceeded"
    if candidate.remaining_usage_ratio is not None and candidate.remaining_usage_ratio <= policy.usage_reserve_ratio:
        return "usage_limit_reached"
    if not policy.auto_routing and candidate.provider.provider_id != policy.default_provider_id:
        return "not_default_provider"
    return None
