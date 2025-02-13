from fastapi import HTTPException, status


class TechnologyError(HTTPException):
    """Base exception for technology domain errors"""

    def __init__(
        self, detail: str, status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR
    ):
        super().__init__(status_code=status_code, detail=detail)


class TechnologyNotFoundError(TechnologyError):
    """Raised when technology resource is not found"""

    def __init__(self, detail: str = "Technology not found"):
        super().__init__(detail=detail, status_code=status.HTTP_404_NOT_FOUND)


class TechnologyDatabaseError(TechnologyError):
    """Raised when database operations fail"""

    def __init__(
        self,
        detail: str = "Database operation failed",
        status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
    ):
        super().__init__(detail=detail, status_code=status_code)
