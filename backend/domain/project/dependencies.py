from typing import Annotated

from database.session import SessionDep
from domain.project.project_repo import ProjectRepo
from domain.project.project_service import ProjectService
from fastapi import Depends


def get_project_repo(session: SessionDep) -> ProjectRepo:
    return ProjectRepo(session=session)


def get_project_service(
    repo: ProjectRepo = Depends(get_project_repo),
) -> ProjectService:
    return ProjectService(repo=repo)


ProjectServiceDep = Annotated[ProjectService, Depends(get_project_service)]
