from database.models import Technology
from domain.technology.dependencies import get_technology_service
from domain.technology.exceptions import TechnologyError
from domain.technology.technology_service import TechnologyService
from fastapi import APIRouter, Depends, HTTPException, status

router = APIRouter()


@router.get("/")
async def get_technologies(
    service: TechnologyService = Depends(get_technology_service),
) -> list[Technology]:
    """Get all technologies.

    Returns:
        list[Technology]: List of all available technologies

    Raises:
        HTTPException: If the request fails
    """
    try:
        return service.get_technologies()
    except TechnologyError as e:
        # Domain exceptions are already properly formatted with status code and detail
        raise e
    except Exception as e:
        # Convert unexpected errors to 500 Internal Server Error
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}",
        )
