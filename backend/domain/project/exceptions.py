"""Domain-specific exceptions for the project module."""

from dataclasses import dataclass
from enum import Enum
from typing import Optional

from core.exceptions import BaseDomainError
from fastapi import status


class ErrorCode(str, Enum):
    """Enumeration of possible error codes for better error handling."""

    PROJECT_NOT_FOUND = "PROJECT_NOT_FOUND"
    DATABASE_ERROR = "DATABASE_ERROR"
    VALIDATION_ERROR = "VALIDATION_ERROR"
    DUPLICATE_PROJECT = "DUPLICATE_PROJECT"
    INVALID_OPERATION = "INVALID_OPERATION"


@dataclass
class ProjectNotFoundError(BaseDomainError):
    """Raised when a project resource is not found.

    Examples:
        >>> raise ProjectNotFoundError()  # Uses default message
        >>> raise ProjectNotFoundError("Custom project not found message")
        >>> raise ProjectNotFoundError(
        ...     message="Project {id} was not found in {location}",
        ...     params={"id": "123", "location": "database"}
        ... )
    """

    code: ErrorCode = ErrorCode.PROJECT_NOT_FOUND
    message: str = "Project not found"  # Default message
    status_code: int = status.HTTP_404_NOT_FOUND

    def __init__(self, message: Optional[str] = None, **kwargs):
        """Initialize with optional custom message.

        Args:
            message: Optional custom error message. If not provided, uses default.
            **kwargs: Additional arguments passed to parent (e.g., params, status_code)
        """
        if message is not None:
            kwargs["message"] = message
        super().__init__(**kwargs)


@dataclass
class ProjectDatabaseError(BaseDomainError):
    """Raised when database operations fail."""

    code: ErrorCode = ErrorCode.DATABASE_ERROR
    message: str = "Database operation failed"
    status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR
