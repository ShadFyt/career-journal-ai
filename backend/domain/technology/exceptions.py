"""Domain-specific exceptions for the technology module."""

from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, Optional

from core.exceptions import ErrorDetail
from fastapi import HTTPException, status


class ErrorCode(str, Enum):
    """Enumeration of possible error codes for better error handling."""

    TECHNOLOGY_NOT_FOUND = "TECHNOLOGY_NOT_FOUND"
    DATABASE_ERROR = "DATABASE_ERROR"
    VALIDATION_ERROR = "VALIDATION_ERROR"
    DUPLICATE_TECHNOLOGY = "DUPLICATE_TECHNOLOGY"
    INVALID_OPERATION = "INVALID_OPERATION"


@dataclass
class TechnologyError(HTTPException):
    """Base exception for technology domain errors with structured error details.

    Examples:
        >>> raise TechnologyError(
        ...     code=ErrorCode.DATABASE_ERROR,
        ...     message="Failed to connect to database",
        ...     status_code=status.HTTP_503_SERVICE_UNAVAILABLE
        ... )
    """

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
        super().__init__(status_code=self.status_code, detail=detail.model_dump())


@dataclass
class TechnologyNotFoundError(TechnologyError):
    """Raised when a technology resource is not found.

    Examples:
        >>> raise TechnologyNotFoundError(
        ...     message="Technology {id} was not found in {location}",
        ...     params={"id": "123", "location": "database"}
        ... )
    """

    code: ErrorCode = ErrorCode.TECHNOLOGY_NOT_FOUND
    message: str = "Technology not found"
    status_code: int = status.HTTP_404_NOT_FOUND

    def __init__(self, **kwargs):
        """Initialize with optional custom message and parameters.

        Args:
            **kwargs: Arguments passed to parent (e.g., message, params)
        """
        super().__init__(
            code=self.code,
            message=kwargs.get("message", self.message),
            params=kwargs.get("params"),
            status_code=kwargs.get("status_code", self.status_code),
        )


@dataclass
class TechnologyDatabaseError(TechnologyError):
    """Raised when database operations fail.

    Examples:
        >>> raise TechnologyDatabaseError(
        ...     message="Failed to create technology: {error}",
        ...     params={"error": "Duplicate entry"},
        ...     status_code=status.HTTP_400_BAD_REQUEST
        ... )
    """

    code: ErrorCode = ErrorCode.DATABASE_ERROR
    message: str = "Database operation failed"
    status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR

    def __init__(self, **kwargs):
        """Initialize with optional custom message and parameters.

        Args:
            **kwargs: Arguments passed to parent (e.g., message, params, status_code)
        """
        super().__init__(
            code=kwargs.get("code", self.code),
            message=kwargs.get("message", self.message),
            params=kwargs.get("params"),
            status_code=kwargs.get("status_code", self.status_code),
        )
