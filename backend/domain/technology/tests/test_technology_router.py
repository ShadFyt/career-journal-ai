"""Tests for the technology router endpoints."""

from mailbox import Message

import pytest
from database.models import Technology
from domain.technology.dependencies import get_technology_service
from domain.technology.exceptions import (
    TechnologyDatabaseError,
    TechnologyNotFoundError,
)
from domain.technology.technology_models import Technology_Create, TechnologyWithCount
from domain.technology.technology_router import router
from domain.technology.technology_service import TechnologyService
from enums import Language
from fastapi import FastAPI, status
from fastapi.testclient import TestClient

# Prepare mock data
mock_technologies = [
    TechnologyWithCount(
        id="1",
        name="Python",
        description="Programming language",
        language=Language.PYTHON,
        usage_count=2,
    ),
    TechnologyWithCount(
        id="2",
        name="JavaScript",
        description="Web language",
        language=Language.JAVASCRIPT,
        usage_count=1,
    ),
]


@pytest.fixture
def mock_technology_service(mocker):
    """Create a mock technology service."""
    return mocker.Mock(spec=TechnologyService)


@pytest.fixture
def app(mock_technology_service):
    """Create a FastAPI test application."""
    app = FastAPI()
    app.include_router(router, prefix="/api/technologies")

    # Override the service dependency
    app.dependency_overrides[get_technology_service] = lambda: mock_technology_service
    return app


@pytest.fixture
def client(app):
    """Create a test client."""
    return TestClient(app)


def test_get_technologies_success(client, mock_technology_service):
    """Test successful GET /api/technologies."""
    mock_technology_service.get_technologies.return_value = mock_technologies

    # Make request
    response = client.get("/api/technologies")

    # Verify response
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) == 2
    assert data[0]["name"] == "Python"
    assert data[1]["name"] == "JavaScript"
    mock_technology_service.get_technologies.assert_called_once_with(None)


def test_get_technologies_with_filter(client, mock_technology_service):
    """Test GET /api/technologies with language filter."""
    # Setup mock return value
    filtered_technologies = [
        t for t in mock_technologies if t.language == Language.PYTHON
    ]
    mock_technology_service.get_technologies.return_value = filtered_technologies

    # Make request with filter
    response = client.get(
        "/api/technologies", params={"language": Language.PYTHON.value}
    )

    # Verify response
    assert response.status_code == status.HTTP_200_OK
    mock_technology_service.get_technologies.assert_called_once_with(Language.PYTHON)


def test_get_technologies_handles_error(client, mock_technology_service):
    """Test error handling in GET /api/technologies."""
    # Setup mock to raise error
    mock_technology_service.get_technologies.side_effect = TechnologyDatabaseError(
        message="Database error",
    )

    # Make request
    response = client.get("/api/technologies")

    error_detail = response.json()["detail"]

    # Verify error response
    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    assert error_detail["message"] == "Database error"


def test_add_technology_success(client, mock_technology_service):
    """Test successful POST /api/technologies."""
    # Prepare test data
    new_tech = Technology_Create(
        name="TypeScript",
        description="JavaScript with types",
        language=Language.JAVASCRIPT,
    )
    mock_result = Technology(
        id="new-id",
        name=new_tech.name,
        description=new_tech.description,
        language=new_tech.language,
    )
    mock_technology_service.add_technology.return_value = mock_result

    # Make request
    response = client.post("/api/technologies", json=new_tech.model_dump())

    # Verify response
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["id"] == "new-id"
    assert data["name"] == new_tech.name
    mock_technology_service.add_technology.assert_called_once()


def test_add_technology_validation_error(client):
    """Test POST /api/technologies with invalid data."""
    # Make request with missing required field
    response = client.post("/api/technologies", json={})

    # Verify validation error
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_add_technology_handles_error(client, mock_technology_service):
    """Test error handling in POST /api/technologies."""
    # Setup mock to raise error
    mock_technology_service.add_technology.side_effect = TechnologyDatabaseError(
        message="Duplicate name",
        status_code=status.HTTP_400_BAD_REQUEST,
    )

    # Make request
    response = client.post(
        "/api/technologies",
        json={"name": "Existing", "description": "Test"},
    )

    # Verify error response
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    error_detail = response.json()["detail"]
    assert error_detail["message"] == "Duplicate name"


def test_delete_technology_success(client, mock_technology_service):
    """Test successful DELETE /api/technologies/{id}."""
    # Make request
    response = client.delete("/api/technologies/1")

    # Verify response
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert response.content == b""  # No content for successful delete
    mock_technology_service.delete_technology.assert_called_once_with("1")


def test_delete_technology_not_found(client, mock_technology_service):
    """Test DELETE /api/technologies/{id} with non-existent ID."""
    # Setup mock to raise not found error
    mock_technology_service.delete_technology.side_effect = TechnologyNotFoundError()

    # Make request
    response = client.delete("/api/technologies/non-existent")

    # Verify error response
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_delete_technology_with_entries(client, mock_technology_service):
    """Test DELETE /api/technologies/{id} with journal entries."""
    # Setup mock to raise error
    mock_technology_service.delete_technology.side_effect = TechnologyDatabaseError(
        message="Cannot delete: has entries",
        status_code=status.HTTP_400_BAD_REQUEST,
    )

    # Make request
    response = client.delete("/api/technologies/1")

    # Verify error response
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    error_detail = response.json()["detail"]
    assert error_detail["message"] == "Cannot delete: has entries"
