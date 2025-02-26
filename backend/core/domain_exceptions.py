"""Common domain exception utilities for creating consistent domain exceptions."""

from typing import Dict, Type

from core.exceptions import BaseDomainError, create_domain_exception
from fastapi import status


def create_not_found_exception(
    domain_name: str,
    error_code: str,
    message: str = None,
) -> Type[BaseDomainError]:
    """Create a standard not found exception for a domain.

    Args:
        domain_name: The domain name (e.g., 'User', 'Project')
        error_code: The error code to use
        message: Optional custom message, defaults to '{domain_name} not found'

    Returns:
        A new exception class for not found errors
    """
    if message is None:
        message = f"{domain_name} not found"

    return create_domain_exception(
        name=f"{domain_name}NotFoundError",
        code=error_code,
        message=message,
        status_code=status.HTTP_404_NOT_FOUND,
    )


def create_database_error(
    domain_name: str,
    error_code: str,
    message: str = None,
) -> Type[BaseDomainError]:
    """Create a standard database error exception for a domain.

    Args:
        domain_name: The domain name (e.g., 'User', 'Project')
        error_code: The error code to use
        message: Optional custom message, defaults to 'Database operation failed'

    Returns:
        A new exception class for database errors
    """
    if message is None:
        message = "Database operation failed"

    return create_domain_exception(
        name=f"{domain_name}DatabaseError",
        code=error_code,
        message=message,
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )


def create_validation_error(
    domain_name: str,
    error_code: str,
    message: str = None,
) -> Type[BaseDomainError]:
    """Create a standard validation error exception for a domain.

    Args:
        domain_name: The domain name (e.g., 'User', 'Project')
        error_code: The error code to use
        message: Optional custom message, defaults to 'Validation failed'

    Returns:
        A new exception class for validation errors
    """
    if message is None:
        message = "Validation failed"

    return create_domain_exception(
        name=f"{domain_name}ValidationError",
        code=error_code,
        message=message,
        status_code=status.HTTP_400_BAD_REQUEST,
    )


def create_duplicate_error(
    domain_name: str,
    error_code: str,
    message: str = None,
) -> Type[BaseDomainError]:
    """Create a standard duplicate error exception for a domain.

    Args:
        domain_name: The domain name (e.g., 'User', 'Project')
        error_code: The error code to use
        message: Optional custom message, defaults to '{domain_name} already exists'

    Returns:
        A new exception class for duplicate errors
    """
    if message is None:
        message = f"{domain_name} already exists"

    return create_domain_exception(
        name=f"Duplicate{domain_name}Error",
        code=error_code,
        message=message,
        status_code=status.HTTP_409_CONFLICT,
    )


def create_domain_exceptions(
    domain_name: str,
    error_codes: Dict[str, str],
) -> Dict[str, Type[BaseDomainError]]:
    """Create a standard set of domain exceptions.

    Args:
        domain_name: The domain name (e.g., 'User', 'Project')
        error_codes: A dictionary mapping exception types to error codes

    Returns:
        A dictionary of exception classes
    """
    exceptions = {}

    if "not_found" in error_codes:
        exceptions["not_found"] = create_not_found_exception(
            domain_name=domain_name,
            error_code=error_codes["not_found"],
        )

    if "database_error" in error_codes:
        exceptions["database_error"] = create_database_error(
            domain_name=domain_name,
            error_code=error_codes["database_error"],
        )

    if "validation_error" in error_codes:
        exceptions["validation_error"] = create_validation_error(
            domain_name=domain_name,
            error_code=error_codes["validation_error"],
        )

    if "duplicate" in error_codes:
        exceptions["duplicate"] = create_duplicate_error(
            domain_name=domain_name,
            error_code=error_codes["duplicate"],
        )

    return exceptions
