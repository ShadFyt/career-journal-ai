from database.models import Project
from domain.project.dependencies import get_project_service
from domain.project.exceptions import ProjectError
from domain.project.project_models import Project_Create, Project_Read
from domain.project.project_service import ProjectService
from fastapi import APIRouter, Depends
from starlette import status

router = APIRouter(prefix="/projects", tags=["projects"])


@router.get("")
async def get_projects(
    service: ProjectService = Depends(get_project_service),
) -> list[Project_Read]:
    """Get all projects sorted by last entry date and name.

    Returns:
        list[Project_Read]: List of all projects

    Raises:
        ProjectDatabaseError: If database operation fails
    """
    try:
        return service.get_projects()
    except ProjectError as e:
        raise e


@router.post("", status_code=status.HTTP_201_CREATED)
async def add_project(
    project: Project_Create,
    service: ProjectService = Depends(get_project_service),
) -> Project_Read:
    """Add a new project.

    Args:
        project: Project to add
        service: Project service instance

    Returns:
        Project_Read: The newly created project
    """
    try:
        return service.add_project(project)
    except ProjectError as e:
        raise e


@router.get("/{id}")
async def get_project(
    id: str,
    service: ProjectService = Depends(get_project_service),
) -> Project:
    """Get a single project by ID.

    Args:
        id: Project ID
        service: Project service instance

    Returns:
        Project_Read: The requested project
    """
    try:
        return service.get_project(id)
    except ProjectError as e:
        raise e
