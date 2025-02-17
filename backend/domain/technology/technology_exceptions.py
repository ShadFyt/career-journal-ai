"""Domain-specific exceptions for the technology module."""

from dataclasses import dataclass
from enum import Enum

from core.exceptions import BaseDomainError
from fastapi import status


class ErrorCode(str, Enum):
    """Enumeration of possible error codes for better error handling."""

    TECHNOLOGY_NOT_FOUND = "TECHNOLOGY_NOT_FOUND"
    DATABASE_ERROR = "DATABASE_ERROR"
    VALIDATION_ERROR = "VALIDATION_ERROR"
    DUPLICATE_TECHNOLOGY = "DUPLICATE_TECHNOLOGY"
    INVALID_OPERATION = "INVALID_OPERATION"


@dataclass
class TechnologyNotFoundError(BaseDomainError):
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
class TechnologyDatabaseError(BaseDomainError):
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
