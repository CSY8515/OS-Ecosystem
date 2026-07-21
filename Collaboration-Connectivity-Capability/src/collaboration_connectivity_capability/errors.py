"""Typed capability errors; raw connector exceptions never cross the boundary."""

from .enums import ErrorCode


class CollaborationConnectivityError(Exception):
    def __init__(self, code: ErrorCode, message: str, *, retryable: bool = False) -> None:
        super().__init__(message)
        self.code = code
        self.retryable = retryable


class UnsupportedOperationError(CollaborationConnectivityError):
    def __init__(self, operation: str) -> None:
        super().__init__(ErrorCode.UNSUPPORTED_OPERATION, f"Unsupported operation: {operation}")
