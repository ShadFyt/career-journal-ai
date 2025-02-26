"""Tests for the project repository."""

import pytest
import pytest_asyncio
from database.models import Project
from domain.project.project_exceptions import ProjectDatabaseError, ProjectNotFoundError
from domain.project.project_repo import ProjectRepo
from domain.project.project_schema import ProjectCreate, ProjectUpdate
from fastapi import status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm.session import Session as SessionDep

mock_user_id = "123"


@pytest_asyncio.fixture
async def sample_projects(db_session: SessionDep) -> list[Project]:
    """Create sample projects for testing."""
    projects = [
        Project(
            id="1",
            name="AI Assistant",
            description="Building an AI assistant",
            user_id=mock_user_id,
        ),
        Project(
            id="2",
            name="E-commerce Platform",
            description="Developing an online store",
            user_id=mock_user_id,
        ),
    ]
    for project in projects:
        db_session.add(project)
        await db_session.commit()
    return projects


@pytest.mark.asyncio
async def test_get_project_success(project_repo: ProjectRepo, sample_projects):
    """Test successfully getting a project by ID."""
    project = await project_repo.get_project(sample_projects[0].id)
    assert project is not None
    assert project.id == sample_projects[0].id
    assert project.name == sample_projects[0].name
    assert project.description == sample_projects[0].description


@pytest.mark.asyncio
async def test_get_project_not_found(project_repo: ProjectRepo):
    """Test getting a non-existent project raises correct error."""
    with pytest.raises(ProjectNotFoundError) as exc_info:
        await project_repo.get_project("non-existent-id")

    error = exc_info.value

    assert error.status_code == status.HTTP_404_NOT_FOUND
    # assert "not found" in str(error.message)


@pytest.mark.asyncio
async def test_add_project_success(project_repo: ProjectRepo):
    """Test successfully adding a new project."""
    new_project = ProjectCreate(
        name="New Project",
        description="Project description",
        user_id=mock_user_id,
    )
    result = await project_repo.add_project(new_project)
    assert result is not None
    assert result.name == new_project.name
    assert result.description == new_project.description
    assert isinstance(result, Project)


@pytest.mark.asyncio
async def test_add_project_database_error(project_repo: ProjectRepo, mocker):
    """Test handling of database errors when adding project."""
    mocker.patch.object(
        project_repo.session, "add", side_effect=SQLAlchemyError("Database error")
    )
    with pytest.raises(ProjectDatabaseError) as exc_info:
        await project_repo.add_project(
            ProjectCreate(name="Test", description="Test", user_id=mock_user_id)
        )
    assert "Failed to add project" in str(exc_info.value)


@pytest.mark.asyncio
async def test_update_project_success(project_repo: ProjectRepo, sample_projects):
    """Test successfully updating a project."""
    updated_data = ProjectUpdate(
        name="Updated Name",
        description="Updated Description",
    )
    result = await project_repo.update_project(sample_projects[0].id, updated_data)
    assert result is not None
    assert result.name == updated_data.name
    assert result.description == updated_data.description


@pytest.mark.asyncio
async def test_delete_project_not_found(project_repo: ProjectRepo):
    """Test deleting a non-existent project raises correct error."""
    with pytest.raises(ProjectNotFoundError) as exc_info:
        await project_repo.delete_project("non-existent-id")
    assert exc_info.value.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio
async def test_delete_project_database_error(
    project_repo: ProjectRepo, sample_projects, mocker
):
    """Test handling of database errors when deleting project."""
    mocker.patch.object(
        project_repo.session, "exec", side_effect=SQLAlchemyError("Database error")
    )
    with pytest.raises(ProjectDatabaseError) as exc_info:
        await project_repo.delete_project(sample_projects[0].id)
    assert "Failed to delete project" in str(exc_info.value)
