from core.exceptions import BaseDomainError
from database.models import Project
from domain.project.project_dependencies import ProjectServiceDep
from domain.project.project_schema import ProjectCreate, ProjectUpdate
from fastapi import APIRouter, status

router = APIRouter()


@router.get("")
async def get_projects(
    service: ProjectServiceDep,
) -> list[Project]:
    """Get all projects sorted by last entry date and name.

    Returns:
        list[Project]: List of all projects

    Raises:
        ProjectDatabaseError: If database operation fails
    """
    try:
        return service.get_projects()
    except BaseDomainError as e:
        raise e


@router.post("", status_code=status.HTTP_201_CREATED)
async def add_project(
    project: ProjectCreate,
    service: ProjectServiceDep,
) -> Project:
    """Add a new project.

    Args:
        project: Project to add
        service: Project service instance

    Returns:
        Project: The newly created project
    """
    try:
        return service.add_project(project)
    except BaseDomainError as e:
        raise e


@router.get("/{id}")
async def get_project(
    id: str,
    service: ProjectServiceDep,
) -> Project:
    """Get a single project by ID.

    Args:
        id: Project ID
        service: Project service instance

    Returns:
        Project: The requested project
    """
    try:
        return service.get_project(id)
    except BaseDomainError as e:
        raise e


@router.patch("/{id}")
async def update_project(
    id: str,
    project: ProjectUpdate,
    service: ProjectServiceDep,
) -> Project:
    """Update an existing project.

    Args:
        id: Project ID
        project: Project update data
        service: Project service instance

    Returns:
        Project: The updated project
    """
    try:
        return service.update_project(id, project)
    except BaseDomainError as e:
        raise e


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_project(
    id: str,
    service: ProjectServiceDep,
) -> None:
    """Delete a project from the database by its ID.

    Args:
        id: Unique identifier of the project to delete
        service: Project service instance

    Raises:
        HTTPException: If the request fails
    """
    try:
        service.delete_project(id)
    except BaseDomainError as e:
        raise e
