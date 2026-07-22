from __future__ import annotations

from typing import Protocol

from .models import ExecutionAttempt, ExecutionSummary


class ExecutionRepository(Protocol):
    def record(self, summary: ExecutionSummary, attempts: tuple[ExecutionAttempt, ...]) -> None: ...
    def recent(self, limit: int = 100) -> tuple[ExecutionSummary, ...]: ...
