from database.models import Technology
from domain.technology.dependencies import get_technology_service
from domain.technology.exceptions import TechnologyError
from domain.technology.technology_models import Technology_Create, TechnologyWithCount
from domain.technology.technology_service import TechnologyService
from enums import Language
from fastapi import APIRouter, Depends, HTTPException, status

router = APIRouter()


@router.get("/")
async def get_technologies(
    language: Language | None = None,
    service: TechnologyService = Depends(get_technology_service),
) -> list[TechnologyWithCount]:
    """Get all technologies with their usage counts.

    Args:
        language: Optional filter by programming language

    Returns:
        list[TechnologyWithCount]: List of technologies with their usage counts

    Raises:
        HTTPException: If the request fails
    """
    try:
        return service.get_technologies(language=language)
    except TechnologyError as e:
        # Domain exceptions are already properly formatted with status code and detail
        raise e
    except Exception as e:
        # Convert unexpected errors to 500 Internal Server Error
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}",
        )


@router.post("/")
async def add_technology(
    technology: Technology_Create,
    service: TechnologyService = Depends(get_technology_service),
) -> Technology:
    """Create a new technology.

    Returns:
        Technology: The newly created technology

    Raises:
        HTTPException: If the request fails
    """
    try:
        return service.add_technology(technology)
    except TechnologyError as e:
        # Domain exceptions are already properly formatted with status code and detail
        raise e
    except Exception as e:
        # Convert unexpected errors to 500 Internal Server Error
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}",
        )


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_technology(
    id: str,
    service: TechnologyService = Depends(get_technology_service),
) -> None:
    """Delete a technology from the database by its ID.

    Args:
        id: Unique identifier of the technology to delete

    Raises:
        HTTPException: If the request fails
    """
    try:
        service.delete_technology(id)
    except TechnologyError as e:
        # Domain exceptions are already properly formatted with status code and detail
        raise e
    except Exception as e:
        # Convert unexpected errors to 500 Internal Server Error
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}",
        )
