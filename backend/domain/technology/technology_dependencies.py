from typing import Annotated

from database.session import SessionDep
from domain.technology.technology_repo import TechnologyRepo
from domain.technology.technology_service import TechnologyService
from fastapi import Depends


def get_technology_repo(session: SessionDep) -> TechnologyRepo:
    return TechnologyRepo(session=session)


def get_technology_service(
    repo: TechnologyRepo = Depends(get_technology_repo),
) -> TechnologyService:
    return TechnologyService(repo=repo)


TechnologyServiceDep = Annotated[TechnologyService, Depends(get_technology_service)]
