from database.models import Technology
from domain.technology.dependencies import TechnologyServiceDep
from domain.technology.exceptions import TechnologyError
from domain.technology.technology_models import Technology_Create, TechnologyWithCount
from enums import Language
from fastapi import APIRouter, status

router = APIRouter(prefix="/technologies", tags=["technologies"])


@router.get("")
async def get_technologies(
    service: TechnologyServiceDep,
    language: Language | None = None,
) -> list[TechnologyWithCount]:
    """Get all technologies with their usage counts.

    Args:
        language: Optional filter by programming language
        service: Technology service instance

    Returns:
        list[TechnologyWithCount]: List of technologies with their usage counts
    """
    try:
        return service.get_technologies(language)
    except TechnologyError as e:
        # Domain exceptions are already properly formatted with status code and detail
        raise e


@router.post("", status_code=status.HTTP_201_CREATED)
async def add_technology(
    technology: Technology_Create,
    service: TechnologyServiceDep,
) -> Technology:
    """Add a new technology.

    Args:
        technology: Technology to add
        service: Technology service instance

    Returns:
        Technology: The newly created technology
    """
    try:
        return service.add_technology(technology)
    except TechnologyError as e:
        raise e


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_technology(
    id: str,
    service: TechnologyServiceDep,
) -> None:
    """Delete a technology from the database by its ID.

    Args:
        id: Unique identifier of the technology to delete
        service: Technology service instance

    Raises:
        HTTPException: If the request fails
    """
    try:
        service.delete_technology(id)
    except TechnologyError as e:
        raise e
