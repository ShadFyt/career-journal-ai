"""Domain-specific exceptions for the user module."""

from enum import Enum

from core.domain_exceptions import create_domain_exceptions


class UserErrorCode(str, Enum):
    """Enumeration of possible error codes for better error handling."""

    USER_NOT_FOUND = "user.not_found"
    DATABASE_ERROR = "user.database_error"
    VALIDATION_ERROR = "user.validation_error"
    DUPLICATE_USER = "user.duplicate"


# Create all domain exceptions at once
exceptions = create_domain_exceptions(
    domain_name="User",
    error_codes={
        "not_found": UserErrorCode.USER_NOT_FOUND,
        "database_error": UserErrorCode.DATABASE_ERROR,
        "validation_error": UserErrorCode.VALIDATION_ERROR,
        "duplicate": UserErrorCode.DUPLICATE_USER,
    },
)

UserNotFoundError = exceptions["not_found"]
UserDatabaseError = exceptions["database_error"]
UserValidationError = exceptions["validation_error"]
DuplicateUserError = exceptions["duplicate"]
