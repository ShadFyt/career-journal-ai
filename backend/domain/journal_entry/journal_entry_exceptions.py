"""Domain-specific exceptions for the journal entry module."""

from dataclasses import dataclass
from enum import Enum
from typing import Optional

from core.exceptions import BaseDomainError
from fastapi import status


class ErrorCode(str, Enum):
    JOURNAL_ENTRY_NOT_FOUND = "journal_entry_not_found"
    DATABASE_ERROR = "DATABASE_ERROR"
    VALIDATION_ERROR = "VALIDATION_ERROR"
    INVALID_OPERATION = "INVALID_OPERATION"


@dataclass
class JournalEntryNotFoundError(BaseDomainError):
    """Raised when a journal entry resource is not found."""

    code: ErrorCode = ErrorCode.JOURNAL_ENTRY_NOT_FOUND
    message: str = "Journal entry not found"
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
class JournalEntryDatabaseError(BaseDomainError):
    """Raised when database operations fail."""

    code: ErrorCode = ErrorCode.DATABASE_ERROR
    message: str = "Database operation failed"
    status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR
