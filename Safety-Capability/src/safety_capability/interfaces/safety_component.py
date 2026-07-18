"""Replaceable safety component interface."""
from abc import ABC, abstractmethod
from typing import Any
from safety_capability.core.context import SafetyExecutionContext
from safety_capability.core.health import HealthReport

class SafetyComponent(ABC):
    """Contract implemented by all registered safety components."""
    component_id: str
    component_name: str
    version: str
    supported_actions: frozenset[str]

    @abstractmethod
    def validate_input(self, context: SafetyExecutionContext) -> None: ...

    @abstractmethod
    def execute(self, context: SafetyExecutionContext) -> dict[str, Any]: ...

    @abstractmethod
    def validate_output(self, output: dict[str, Any], context: SafetyExecutionContext) -> None: ...

    @abstractmethod
    def health_check(self) -> HealthReport: ...

    @abstractmethod
    def metadata(self) -> dict[str, Any]: ...
