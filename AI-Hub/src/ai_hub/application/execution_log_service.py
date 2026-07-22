from ai_hub.domain.executions import ExecutionAttempt, ExecutionRepository, ExecutionSummary


class ExecutionLogService:
    def __init__(self, repository: ExecutionRepository) -> None:
        self._repository = repository

    def record(self, summary: ExecutionSummary, attempts: tuple[ExecutionAttempt, ...]) -> None:
        self._repository.record(summary, attempts)

    def recent(self, limit: int = 100) -> tuple[ExecutionSummary, ...]:
        return self._repository.recent(limit)
