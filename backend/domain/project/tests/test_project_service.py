"""Tests for the project service."""

import pytest
from domain.project.project_exceptions import ProjectDatabaseError, ProjectNotFoundError
from domain.project.project_repo import ProjectRepo
from domain.project.project_schema import ProjectCreate, ProjectUpdate
from domain.project.project_service import ProjectService
from fastapi import status

mock_user_id = "123"


@pytest.fixture
def mock_project_repo(mocker) -> ProjectRepo:
    """Create a mock project repository."""
    return mocker.Mock(spec=ProjectRepo)


@pytest.fixture
def project_service(mock_project_repo):
    """Create a ProjectService with a mocked repository."""
    return ProjectService(mock_project_repo)


@pytest.mark.asyncio
async def test_create_project_success(project_service, mock_project_repo):
    """Test successful project creation through service."""
    # Prepare test data
    project_data = ProjectCreate(
        name="AI Assistant",
        description="Building an AI assistant",
        user_id=mock_user_id,
    )

    # Setup mock behavior
    mock_project_repo.add_project.return_value = "1"

    # Execute service method
    result = await project_service.add_project(project_data)

    # Verify results
    assert result == "1"
    mock_project_repo.add_project.assert_called_once_with(project_data)


@pytest.mark.asyncio
async def test_create_project_database_error(project_service, mock_project_repo):
    """Test handling database errors during project creation."""
    # Prepare test data
    project_data = ProjectCreate(
        name="AI Assistant",
        description="Building an AI assistant",
        user_id=mock_user_id,
    )

    # Setup mock behavior
    mock_project_repo.add_project.side_effect = ProjectDatabaseError()

    # Execute and verify
    with pytest.raises(ProjectDatabaseError) as exc_info:
        await project_service.add_project(project_data)

    error = exc_info.value
    assert error.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    assert "Database operation failed" in error.message


@pytest.mark.asyncio
async def test_get_project_success(project_service, mock_project_repo):
    """Test successfully retrieving a project through service."""
    # Prepare mock data
    mock_project = {
        "id": "1",
        "name": "AI Assistant",
        "description": "Building an AI assistant",
    }

    # Setup mock behavior
    mock_project_repo.get_project.return_value = mock_project

    # Execute service method
    result = await project_service.get_project("1")

    # Verify results
    assert result == mock_project
    mock_project_repo.get_project.assert_called_once_with("1")


@pytest.mark.asyncio
async def test_get_project_not_found(project_service, mock_project_repo):
    """Test handling project not found error."""
    # Setup mock behavior
    mock_project_repo.get_project.side_effect = ProjectNotFoundError(
        status_code=status.HTTP_404_NOT_FOUND,
        code="PROJECT_NOT_FOUND",
        detail="Project not found",
    )

    # Execute and verify
    with pytest.raises(ProjectNotFoundError) as exc_info:
        await project_service.get_project("non-existent-id")

    error = exc_info.value
    assert error.status_code == status.HTTP_404_NOT_FOUND
    assert error.code == "PROJECT_NOT_FOUND"
    assert "Project not found" in error.message


@pytest.mark.asyncio
async def test_update_project_success(project_service, mock_project_repo):
    """Test successfully updating a project through service."""
    # Prepare test data
    project_update = ProjectUpdate(
        name="Updated AI Assistant", description="Updated description"
    )

    # Setup mock behavior
    mock_project_repo.update_project.return_value = {
        "id": "1",
        "name": "Updated AI Assistant",
        "description": "Updated description",
    }

    # Execute service method
    result = await project_service.update_project("1", project_update)

    # Verify results
    assert result["name"] == "Updated AI Assistant"
    assert result["description"] == "Updated description"
    mock_project_repo.update_project.assert_called_once_with("1", project_update)


@pytest.mark.asyncio
async def test_delete_project_success(project_service, mock_project_repo):
    """Test successfully deleting a project through service."""
    # Setup mock behavior
    mock_project_repo.delete_project.return_value = None

    # Execute service method
    await project_service.delete_project("1")

    # Verify results
    mock_project_repo.delete_project.assert_called_once_with("1")
