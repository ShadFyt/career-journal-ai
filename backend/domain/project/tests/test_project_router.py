"""Tests for the project router endpoints."""

import pytest
from domain.project.project_dependencies import get_project_service
from domain.project.project_exceptions import ProjectDatabaseError, ProjectNotFoundError
from domain.project.project_router import router
from domain.project.project_service import ProjectService
from fastapi import FastAPI, status
from fastapi.testclient import TestClient

mock_user_id = "123"
# Prepare mock data
mock_projects = [
    {
        "id": "1",
        "name": "AI Assistant",
        "description": "Building an AI assistant",
        "is_private": True,
        "last_entry_date": None,
        "link": None,
    },
    {
        "id": "2",
        "name": "E-commerce Platform",
        "description": "Developing an online store",
        "is_private": True,
        "last_entry_date": None,
        "link": None,
    },
]


@pytest.fixture
def mock_project_service(mocker):
    """Create a mock project service."""
    return mocker.Mock(spec=ProjectService)


@pytest.fixture
def app(mock_project_service):
    """Create a FastAPI test application."""
    app = FastAPI()
    app.include_router(router, prefix="/api/projects")

    # Override the service dependency
    app.dependency_overrides[get_project_service] = lambda: mock_project_service
    return app


@pytest.fixture
def client(app):
    """Create a test client."""
    return TestClient(app)


def test_get_projects_success(client, mock_project_service):
    """Test successful retrieval of all projects."""
    # Setup mock behavior
    mock_project_service.get_projects.return_value = mock_projects

    # Execute request
    response = client.get("/api/projects")

    # Verify response
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == mock_projects
    mock_project_service.get_projects.assert_called_once()


def test_get_projects_handles_error(client, mock_project_service):
    """Test error handling when getting projects fails."""
    # Setup mock behavior
    mock_project_service.get_projects.side_effect = ProjectDatabaseError()

    # Execute request
    response = client.get("/api/projects")

    # Verify response
    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    mock_project_service.get_projects.assert_called_once()


def test_add_project_success(client, mock_project_service):
    """Test successful project creation."""
    # Prepare test data
    project_data = {
        "name": "New Project",
        "description": "Test project description",
        "user_id": mock_user_id,
    }
    mock_response = {
        **project_data,
        "id": "3",
        "is_private": False,
        "last_entry_date": None,
        "link": None,
    }

    # Setup mock behavior
    mock_project_service.add_project.return_value = mock_response

    # Execute request
    response = client.post("/api/projects", json=project_data)

    # Verify response
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == mock_response
    mock_project_service.add_project.assert_called_once()


def test_add_project_validation_error(client):
    """Test project creation with invalid data."""
    # Execute request with invalid data (missing required field)
    response = client.post("/api/projects", json={"description": "Missing name"})

    # Verify response
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_add_project_handles_error(client, mock_project_service):
    """Test error handling when project creation fails."""
    # Prepare test data
    project_data = {
        "name": "New Project",
        "description": "Test project description",
        "user_id": mock_user_id,
    }

    # Setup mock behavior
    mock_project_service.add_project.side_effect = ProjectDatabaseError()

    # Execute request
    response = client.post("/api/projects", json=project_data)

    # Verify response
    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    mock_project_service.add_project.assert_called_once()


def test_get_project_success(client, mock_project_service):
    """Test successful retrieval of a single project."""
    # Setup mock behavior
    mock_project_service.get_project.return_value = mock_projects[0]

    # Execute request
    response = client.get("/api/projects/1")

    # Verify response
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == mock_projects[0]
    mock_project_service.get_project.assert_called_once_with("1")


def test_get_project_not_found(client, mock_project_service):
    """Test getting a non-existent project."""
    # Setup mock behavior
    mock_project_service.get_project.side_effect = ProjectNotFoundError()

    # Execute request
    response = client.get("/api/projects/999")

    # Verify response
    assert response.status_code == status.HTTP_404_NOT_FOUND
    mock_project_service.get_project.assert_called_once_with("999")


def test_update_project_success(client, mock_project_service):
    """Test successful project update."""
    # Prepare test data
    update_data = {"name": "Updated Project", "description": "Updated description"}
    mock_response = {
        **update_data,
        "id": "1",
        "is_private": False,
        "last_entry_date": None,
        "link": None,
    }

    # Setup mock behavior
    mock_project_service.update_project.return_value = mock_response

    # Execute request
    response = client.patch("/api/projects/1", json=update_data)

    # Verify response
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == mock_response
    mock_project_service.update_project.assert_called_once()


def test_update_project_not_found(client, mock_project_service):
    """Test updating a non-existent project."""
    # Prepare test data
    update_data = {"name": "Updated Project", "description": "Updated description"}

    # Setup mock behavior
    mock_project_service.update_project.side_effect = ProjectNotFoundError()

    # Execute request
    response = client.patch("/api/projects/999", json=update_data)

    # Verify response
    assert response.status_code == status.HTTP_404_NOT_FOUND
    mock_project_service.update_project.assert_called_once()


def test_delete_project_success(client, mock_project_service):
    """Test successful project deletion."""
    # Setup mock behavior
    mock_project_service.delete_project.return_value = None

    # Execute request
    response = client.delete("/api/projects/1")

    # Verify response
    assert response.status_code == status.HTTP_204_NO_CONTENT
    mock_project_service.delete_project.assert_called_once_with("1")


def test_delete_project_not_found(client, mock_project_service):
    """Test deleting a non-existent project."""
    # Setup mock behavior
    mock_project_service.delete_project.side_effect = ProjectNotFoundError()

    # Execute request
    response = client.delete("/api/projects/999")

    # Verify response
    assert response.status_code == status.HTTP_404_NOT_FOUND
    mock_project_service.delete_project.assert_called_once_with("999")
