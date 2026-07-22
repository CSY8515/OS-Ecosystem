from ai_hub.domain.executions import ExecutionRepository
from ai_hub.domain.usage import UsageAnalytics, build_usage_analytics


class UsageAnalyticsService:
    def __init__(self, repository: ExecutionRepository) -> None:
        self._repository = repository

    def summarize_recent(self, limit: int = 100) -> UsageAnalytics:
        return build_usage_analytics(self._repository.recent(limit))
