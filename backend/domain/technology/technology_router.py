from authx import TokenPayload

from core.exceptions import BaseDomainError
from database.models import Technology
from domain.technology.technology_dependencies import TechnologyServiceDep
from domain.technology.technology_schema import Technology_Create, TechnologyWithCount
from enums import Language
from fastapi import APIRouter, status, Depends
from domain.auth.auth_config import security


router = APIRouter()


@router.get("", response_model=list[TechnologyWithCount])
async def get_technologies(
    service: TechnologyServiceDep,
    language: Language | None = None,
    payload: TokenPayload = Depends(security.access_token_required),
):
    """Get all technologies with their usage counts.

    Args:
        language: Optional filter by programming language
        service: Technology service instance
        payload: Authentication payload

    Returns:
        list[TechnologyWithCount]: List of technologies with their usage counts
    """
    try:
        return await service.get_technologies(
            user_id=payload.user_id, language=language
        )
    except BaseDomainError as e:
        # Domain exceptions are already properly formatted with status code and detail
        raise e


@router.post("", status_code=status.HTTP_201_CREATED, response_model=Technology)
async def add_technology(
    technology: Technology_Create,
    service: TechnologyServiceDep,
    payload: TokenPayload = Depends(security.access_token_required),
):
    """Add a new technology.

    Args:
        technology: Technology to add
        service: Technology service instance
        payload: Authentication payload

    Returns:
        Technology: The newly created technology
    """
    try:
        return await service.add_technology(technology, payload.user_id)
    except BaseDomainError as e:
        raise e


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_technology(
    tech_id: str,
    service: TechnologyServiceDep,
) -> None:
    """Delete a technology from the database by its ID.

    Args:
        tech_id: Unique identifier of the technology to delete
        service: Technology service instance

    Raises:
        HTTPException: If the request fails
    """
    try:
        await service.delete_technology(tech_id)
    except BaseDomainError as e:
        raise e
