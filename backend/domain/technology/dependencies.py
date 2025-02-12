from fastapi import Depends
from database.session import SessionDep
from domain.technology.technology_repo import TechnologyRepo
from domain.technology.technology_service import TechnologyService


def get_technology_repo(session: SessionDep) -> TechnologyRepo:
    return TechnologyRepo(session=session)


def get_technology_service(
    repo: TechnologyRepo = Depends(get_technology_repo),
) -> TechnologyService:
    return TechnologyService(repo=repo)
