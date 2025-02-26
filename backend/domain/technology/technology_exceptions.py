"""Domain-specific exceptions for the technology module."""

from enum import Enum

from core.domain_exceptions import create_domain_exceptions


class ErrorCode(str, Enum):
    """Enumeration of possible error codes for better error handling."""

    TECHNOLOGY_NOT_FOUND = "TECHNOLOGY_NOT_FOUND"
    DATABASE_ERROR = "DATABASE_ERROR"
    VALIDATION_ERROR = "VALIDATION_ERROR"
    DUPLICATE_TECHNOLOGY = "DUPLICATE_TECHNOLOGY"
    INVALID_OPERATION = "INVALID_OPERATION"


exceptions = create_domain_exceptions(
    domain_name="Technology",
    error_codes={
        "not_found": ErrorCode.TECHNOLOGY_NOT_FOUND,
        "database_error": ErrorCode.DATABASE_ERROR,
        "validation_error": ErrorCode.VALIDATION_ERROR,
        "duplicate": ErrorCode.DUPLICATE_TECHNOLOGY,
    },
)

# Extract exceptions for easier imports
TechnologyNotFoundError = exceptions["not_found"]
TechnologyDatabaseError = exceptions["database_error"]
TechnologyValidationError = exceptions["validation_error"]
DuplicateTechnologyError = exceptions["duplicate"]
