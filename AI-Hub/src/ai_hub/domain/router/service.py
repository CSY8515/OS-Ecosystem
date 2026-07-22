from __future__ import annotations

from collections.abc import Iterable

from ai_hub.domain.providers import InferenceRequest
from .eligibility import exclusion_reason
from .models import RoutingCandidate, RoutingDecision
from .policy import RoutingPolicy
from .scoring import score_candidate


class Router:
    def route(self, request: InferenceRequest, candidates: Iterable[RoutingCandidate], policy: RoutingPolicy) -> RoutingDecision:
        eligible = []
        exclusions = []
        for candidate in candidates:
            reason = exclusion_reason(candidate, request, policy)
            if reason:
                exclusions.append((candidate.model.model_id, reason))
            else:
                eligible.append(score_candidate(candidate, policy))
        eligible.sort(key=lambda item: (
            -item.score,
            item.candidate.model.routing_priority,
            item.candidate.model.model_id,
        ))
        limit = min(len(eligible), 1 + policy.retry_count)
        return RoutingDecision(policy.version, tuple(eligible[:limit]), tuple(sorted(exclusions)))
