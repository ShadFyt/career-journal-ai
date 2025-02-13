import logging

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse


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
