"""Tests for the user router endpoints."""

import pytest
from domain.user.user_dependencies import get_user_service
from domain.user.user_exceptions import (
    DuplicateUserError,
    UserDatabaseError,
    UserNotFoundError,
)
from domain.user.user_router import router
from domain.user.user_service import UserService
from fastapi import FastAPI, status
from fastapi.testclient import TestClient

# Mock user data for response validation
mock_users = [
    {
        "id": "1",
        "email": "john.doe@example.com",
        "first_name": "John",
        "last_name": "Doe",
    },
    {
        "id": "2",
        "email": "jane.smith@example.com",
        "first_name": "Jane",
        "last_name": "Smith",
    },
]


@pytest.fixture
def mock_user_service(mocker):
    """Create a mock user service."""
    return mocker.Mock(spec=UserService)


@pytest.fixture
def app(mock_user_service):
    """Create a FastAPI test application."""
    app = FastAPI()
    app.include_router(router, prefix="/api/users")

    # Override the service dependency
    app.dependency_overrides[get_user_service] = lambda: mock_user_service
    return app


@pytest.fixture
def client(app):
    """Create a test client."""
    return TestClient(app)


def test_get_users_success(client, mock_user_service):
    """Test successful retrieval of all users."""
    # Setup mock behavior
    mock_user_service.get_users.return_value = mock_users

    # Execute request
    response = client.get("/api/users")

    # Verify response
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == mock_users
    mock_user_service.get_users.assert_called_once()


def test_get_users_handles_error(client, mock_user_service):
    """Test error handling when getting users fails."""
    # Setup mock behavior
    mock_user_service.get_users.side_effect = UserDatabaseError(
        message="Failed to fetch users"
    )

    # Execute request
    response = client.get("/api/users")

    # Verify response
    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR

    mock_user_service.get_users.assert_called_once()


def test_add_user_success(client, mock_user_service):
    """Test successful user creation."""
    # Prepare test data
    user_data = {
        "email": "new.user@example.com",
        "first_name": "New",
        "last_name": "User",
        "password": "securepassword123",
    }
    mock_response = {
        "id": "3",
        "email": "new.user@example.com",
        "first_name": "New",
        "last_name": "User",
    }

    # Setup mock behavior
    mock_user_service.add_user.return_value = mock_response

    # Execute request
    response = client.post("/api/users", json=user_data)

    # Verify response
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == mock_response
    mock_user_service.add_user.assert_called_once()
    # Verify the service was called with the correct data
    called_with = mock_user_service.add_user.call_args[0][0]
    assert called_with.email == user_data["email"]
    assert called_with.first_name == user_data["first_name"]
    assert called_with.last_name == user_data["last_name"]
    assert called_with.password == user_data["password"]


def test_add_user_validation_error(client):
    """Test user creation with invalid data."""
    # Missing required fields
    user_data = {
        "email": "invalid@example.com",
        # Missing first_name, last_name, and password
    }

    # Execute request
    response = client.post("/api/users", json=user_data)

    # Verify response
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    # The validation error details should be in the response
    assert "first_name" in response.text
    assert "last_name" in response.text
    assert "password" in response.text


def test_add_user_handles_duplicate_error(client, mock_user_service):
    """Test error handling when user creation fails due to duplicate email."""
    # Prepare test data
    user_data = {
        "email": "existing@example.com",
        "first_name": "Existing",
        "last_name": "User",
        "password": "securepassword123",
    }

    # Setup mock behavior
    mock_user_service.add_user.side_effect = DuplicateUserError(
        message="User with email 'existing@example.com' already exists"
    )

    # Execute request
    response = client.post("/api/users", json=user_data)

    # Verify response
    error_detail = response.json()["detail"]
    assert response.status_code == status.HTTP_409_CONFLICT
    # assert "already exists" in response.json()["detail"]
    assert error_detail["code"] == "user.duplicate"
    mock_user_service.add_user.assert_called_once()


def test_get_user_success(client, mock_user_service):
    """Test successful retrieval of a single user."""
    # Setup mock behavior
    mock_user_service.get_user.return_value = mock_users[0]

    # Execute request
    response = client.get(f"/api/users/{mock_users[0]['id']}")

    # Verify response
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == mock_users[0]
    mock_user_service.get_user.assert_called_once_with(mock_users[0]["id"])


def test_get_user_not_found(client, mock_user_service):
    """Test getting a non-existent user."""
    # Setup mock behavior
    user_id = "non-existent-id"
    mock_user_service.get_user.side_effect = UserNotFoundError(
        message=f"User with ID '{user_id}' not found"
    )

    # Execute request
    response = client.get(f"/api/users/{user_id}")

    # Verify response
    assert response.status_code == status.HTTP_404_NOT_FOUND
    error_detail = response.json()["detail"]
    assert error_detail["code"] == "user.not_found"
    mock_user_service.get_user.assert_called_once_with(user_id)


def test_update_user_success(client, mock_user_service):
    """Test successful user update."""
    # Prepare test data
    user_id = mock_users[0]["id"]
    update_data = {
        "email": "updated.email@example.com",
        "first_name": "Updated",
        "last_name": "Name",
    }
    mock_response = {
        "id": user_id,
        "email": "updated.email@example.com",
        "first_name": "Updated",
        "last_name": "Name",
    }

    # Setup mock behavior
    mock_user_service.update_user.return_value = mock_response

    # Execute request
    response = client.patch(f"/api/users/{user_id}", json=update_data)

    # Verify response
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == mock_response
    mock_user_service.update_user.assert_called_once()
    # Verify the service was called with the correct data
    called_with_id, called_with_data = mock_user_service.update_user.call_args[0]
    assert called_with_id == user_id
    assert called_with_data.email == update_data["email"]
    assert called_with_data.first_name == update_data["first_name"]
    assert called_with_data.last_name == update_data["last_name"]


def test_update_user_not_found(client, mock_user_service):
    """Test updating a non-existent user."""
    # Prepare test data
    user_id = "non-existent-id"
    update_data = {
        "email": "updated.email@example.com",
        "first_name": "Updated",
        "last_name": "Name",
    }

    # Setup mock behavior
    mock_user_service.update_user.side_effect = UserNotFoundError(
        message=f"User with ID '{user_id}' not found"
    )

    # Execute request
    response = client.patch(f"/api/users/{user_id}", json=update_data)

    # Verify response
    assert response.status_code == status.HTTP_404_NOT_FOUND
    error_detail = response.json()["detail"]
    assert error_detail["code"] == "user.not_found"
    mock_user_service.update_user.assert_called_once()


def test_delete_user_success(client, mock_user_service):
    """Test successful user deletion."""
    # Setup mock behavior
    user_id = mock_users[0]["id"]
    mock_user_service.delete_user.return_value = None

    # Execute request
    response = client.delete(f"/api/users/{user_id}")

    # Verify response
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert response.content == b""  # No content in response body
    mock_user_service.delete_user.assert_called_once_with(user_id)


def test_delete_user_not_found(client, mock_user_service):
    """Test deleting a non-existent user."""
    # Setup mock behavior
    user_id = "non-existent-id"
    mock_user_service.delete_user.side_effect = UserNotFoundError(
        message=f"User with ID '{user_id}' not found"
    )

    # Execute request
    response = client.delete(f"/api/users/{user_id}")

    # Verify response
    assert response.status_code == status.HTTP_404_NOT_FOUND
    error_detail = response.json()["detail"]
    assert error_detail["code"] == "user.not_found"
    mock_user_service.delete_user.assert_called_once_with(user_id)
