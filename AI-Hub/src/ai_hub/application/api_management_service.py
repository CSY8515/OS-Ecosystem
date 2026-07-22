from ai_hub.domain.callers import CallerRegistration
from ai_hub.domain.common.errors import AIHubError, ErrorCode


class APIManagementService:
    def __init__(self) -> None:
        self._callers: dict[str, CallerRegistration] = {}

    def register(self, caller: CallerRegistration) -> None:
        if caller.caller_id in self._callers:
            raise ValueError("caller is already registered")
        self._callers[caller.caller_id] = caller

    def authorize(self, caller_id: str, scope: str) -> CallerRegistration:
        caller = self._callers.get(caller_id)
        if caller is None:
            raise AIHubError(ErrorCode.UNAUTHORIZED, "caller is not registered")
        if not caller.enabled or scope not in caller.scopes:
            raise AIHubError(ErrorCode.FORBIDDEN, "caller is not authorized")
        return caller

    def list_callers(self) -> tuple[CallerRegistration, ...]:
        return tuple(self._callers[key] for key in sorted(self._callers))
