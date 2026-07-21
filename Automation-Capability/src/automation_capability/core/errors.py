"""Public Automation Capability error types and codes."""

from enum import Enum


class ErrorCode(str, Enum):
    INVALID_CONTEXT = "INVALID_CONTEXT"
    COMPONENT_NOT_FOUND = "COMPONENT_NOT_FOUND"
    ACTION_NOT_SUPPORTED = "ACTION_NOT_SUPPORTED"
    COMPONENT_DISABLED = "COMPONENT_DISABLED"
    INPUT_VALIDATION_FAILED = "INPUT_VALIDATION_FAILED"
    APPROVAL_REQUIRED = "APPROVAL_REQUIRED"
    SAFETY_REJECTED = "SAFETY_REJECTED"
    EXECUTION_FAILED = "EXECUTION_FAILED"
    OUTPUT_VALIDATION_FAILED = "OUTPUT_VALIDATION_FAILED"


class AutomationCapabilityError(Exception):
    def __init__(self, code: ErrorCode, message: str) -> None:
        super().__init__(message)
        self.code = code


class ContextValidationError(AutomationCapabilityError):
    def __init__(self, message: str) -> None:
        super().__init__(ErrorCode.INVALID_CONTEXT, message)


class InputValidationError(AutomationCapabilityError):
    def __init__(self, message: str) -> None:
        super().__init__(ErrorCode.INPUT_VALIDATION_FAILED, message)


class OutputValidationError(AutomationCapabilityError):
    def __init__(self, message: str) -> None:
        super().__init__(ErrorCode.OUTPUT_VALIDATION_FAILED, message)

