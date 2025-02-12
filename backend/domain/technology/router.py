from database.models import Technology
from domain.technology.dependencies import get_technology_service
from domain.technology.technology_service import TechnologyService
from fastapi import APIRouter, Depends

router = APIRouter()


@router.get("/")
async def get_technologies(
    service: TechnologyService = Depends(get_technology_service),
) -> list[Technology]:
    return service.get_technologies()
