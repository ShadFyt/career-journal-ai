import logging
from dataclasses import dataclass
from typing import Any, Dict, Optional

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
        super().__init__(status_code=self.status_code, detail=detail.dict())


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
