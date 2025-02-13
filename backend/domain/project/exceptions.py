from fastapi import HTTPException, status


class ProjectError(HTTPException):
    """Base exception for project domain errors"""

    def __init__(
        self, detail: str, status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR
    ):
        super().__init__(status_code=status_code, detail=detail)


class ProjectNotFoundError(ProjectError):
    """Raised when project resource is not found"""

    def __init__(
        self,
        detail: str = "Project not found",
        status_code: int = status.HTTP_404_NOT_FOUND,
    ):
        super().__init__(detail=detail, status_code=status_code)


class ProjectDatabaseError(ProjectError):
    """Raised when database operations fail"""

    def __init__(
        self,
        detail: str = "Database operation failed",
        status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
    ):
        super().__init__(detail=detail, status_code=status_code)
