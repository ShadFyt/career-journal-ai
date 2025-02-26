"""Domain-specific exceptions for the project module."""

from enum import Enum

from core.domain_exceptions import create_domain_exception, create_domain_exceptions
from fastapi import status


class ProjectErrorCode(str, Enum):
    """Enumeration of possible error codes for better error handling."""

    PROJECT_NOT_FOUND = "project.not_found"
    DATABASE_ERROR = "project.database_error"
    VALIDATION_ERROR = "project.validation_error"
    DUPLICATE_PROJECT = "project.duplicate"
    INVALID_OPERATION = "project.invalid_operation"


# Create standard domain exceptions
exceptions = create_domain_exceptions(
    domain_name="Project",
    error_codes={
        "not_found": ProjectErrorCode.PROJECT_NOT_FOUND,
        "database_error": ProjectErrorCode.DATABASE_ERROR,
        "validation_error": ProjectErrorCode.VALIDATION_ERROR,
        "duplicate": ProjectErrorCode.DUPLICATE_PROJECT,
    },
)

# Extract exceptions for easier imports
ProjectNotFoundError = exceptions["not_found"]
ProjectDatabaseError = exceptions["database_error"]
ProjectValidationError = exceptions["validation_error"]
DuplicateProjectError = exceptions["duplicate"]


InvalidOperationError = create_domain_exception(
    name="InvalidOperationError",
    code=ProjectErrorCode.INVALID_OPERATION,
    message="Invalid operation",
    status_code=status.HTTP_400_BAD_REQUEST,
)
