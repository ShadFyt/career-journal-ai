"""Domain-specific exceptions for the project module."""

from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, Optional

from core.exceptions import ErrorDetail
from fastapi import HTTPException, status


class ErrorCode(str, Enum):
    """Enumeration of possible error codes for better error handling."""

    PROJECT_NOT_FOUND = "PROJECT_NOT_FOUND"
    DATABASE_ERROR = "DATABASE_ERROR"
    VALIDATION_ERROR = "VALIDATION_ERROR"
    DUPLICATE_PROJECT = "DUPLICATE_PROJECT"
    INVALID_OPERATION = "INVALID_OPERATION"


@dataclass
class ProjectError(HTTPException):
    """Base exception for project domain errors with structured error details."""

    code: ErrorCode
    message: str
    params: Optional[Dict[str, Any]] = None
    status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR

    def __post_init__(self):
        """Initialize the HTTPException with structured error detail."""
        detail = ErrorDetail(
            code=self.code,
            message=self.message,
            params=self.params,
        )
        super().__init__(status_code=self.status_code, detail=detail.dict())


@dataclass
class ProjectNotFoundError(ProjectError):
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
class ProjectDatabaseError(ProjectError):
    """Raised when database operations fail."""

    code: ErrorCode = ErrorCode.DATABASE_ERROR
    message: str = "Database operation failed"
    status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR
