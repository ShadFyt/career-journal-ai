import logging
from dataclasses import dataclass
from typing import Any, Dict, Optional, Type

from fastapi import FastAPI, HTTPException, Request, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel


@dataclass
class BaseDomainError(HTTPException):
    """Base exception for domain errors with structured error details."""

    code: str
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


def create_domain_exception(
    name: str,
    code: str,
    message: str,
    status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
) -> Type[BaseDomainError]:
    """Factory function to create domain-specific exceptions.

    Args:
        name: The name of the exception class (e.g., 'UserNotFound')
        code: The error code
        message: The default error message
        status_code: The HTTP status code to return

    Returns:
        A new exception class that inherits from BaseDomainError
    """

    # Create class attributes in a way that captures the function parameters
    attrs = {
        "code": code,
        "message": message,
        "status_code": status_code,
        "__doc__": f"{name} domain exception.",
        "__module__": __name__,
    }

    # Define the __init__ method that will be added to the class
    def __init__(self, **kwargs):
        """Initialize with optional custom message.

        Args:
            **kwargs: Additional arguments passed to parent (e.g., params, status_code)
        """
        super(self.__class__, self).__init__(
            code=kwargs.get("code", self.code),
            message=kwargs.get("message", self.message),
            params=kwargs.get("params"),
            status_code=kwargs.get("status_code", self.status_code),
        )

    # Add the __init__ method to the attributes
    attrs["__init__"] = __init__

    # Create the class dynamically
    DomainException = type(name, (BaseDomainError,), attrs)

    return DomainException


class ErrorDetail(BaseModel):
    """Structured error details for better error reporting."""

    code: str
    message: str
    params: Optional[Dict[str, Any]] = None


def add_exception_handlers(app: FastAPI) -> None:
    """Add global exception handlers to the FastAPI application.

    Args:
        app: FastAPI application instance
    """

    @app.exception_handler(Exception)
    async def global_exception_handler(
        request: Request, exc: Exception
    ) -> JSONResponse:
        """Handle all uncaught exceptions globally.

        Args:
            request: FastAPI request instance
            exc: The raised exception

        Returns:
            JSONResponse with 500 status code and error details
        """
        logging.error(f"Uncaught server error: {str(exc)}")

        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": f"Internal server error: {str(exc)}"},
        )
