"""Tests for the user service."""

import pytest
from database.models import User
from domain.user.user_exceptions import (
    DuplicateUserError,
    UserDatabaseError,
    UserNotFoundError,
)
from domain.user.user_schema import UserCreate, UserUpdate
from fastapi import status


@pytest.mark.asyncio
async def test_get_users_success(user_service, mocker):
    """Test successfully retrieving all users through service."""
    # Prepare mock data
    mock_users = [
        User(
            id="1",
            email="john.doe@example.com",
            first_name="John",
            last_name="Doe",
            password="hashed_password1",
        ),
        User(
            id="2",
            email="jane.smith@example.com",
            first_name="Jane",
            last_name="Smith",
            password="hashed_password2",
        ),
    ]

    # Setup mock behavior
    mocker.patch.object(user_service.user_repo, "get_users", return_value=mock_users)

    # Execute service method
    result = await user_service.get_users()

    # Verify results
    assert result == mock_users
    assert len(result) == 2
    user_service.user_repo.get_users.assert_called_once()


@pytest.mark.asyncio
async def test_get_users_database_error(user_service, mocker):
    """Test handling database errors when retrieving all users."""
    # Setup mock behavior
    mocker.patch.object(
        user_service.user_repo,
        "get_users",
        side_effect=UserDatabaseError(message="Failed to fetch users"),
    )

    # Execute and verify
    with pytest.raises(UserDatabaseError) as exc_info:
        await user_service.get_users()

    error = exc_info.value
    assert error.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    assert "Failed to fetch users" in error.message


@pytest.mark.asyncio
async def test_get_user_success(user_service, mocker):
    """Test successfully retrieving a user by ID through service."""
    # Prepare mock data
    mock_user = User(
        id="1",
        email="john.doe@example.com",
        first_name="John",
        last_name="Doe",
        password="hashed_password",
    )

    # Setup mock behavior
    mocker.patch.object(user_service.user_repo, "get_user", return_value=mock_user)

    # Execute service method
    result = await user_service.get_user("1")

    # Verify results
    assert result == mock_user
    assert result.id == "1"
    assert result.email == "john.doe@example.com"
    user_service.user_repo.get_user.assert_called_once_with("1")


@pytest.mark.asyncio
async def test_get_user_not_found(user_service, mocker):
    """Test handling user not found error."""
    # Setup mock behavior
    mocker.patch.object(
        user_service.user_repo,
        "get_user",
        side_effect=UserNotFoundError(
            message="User with ID 'non-existent-id' not found"
        ),
    )

    # Execute and verify
    with pytest.raises(UserNotFoundError) as exc_info:
        await user_service.get_user("non-existent-id")

    error = exc_info.value
    assert error.status_code == status.HTTP_404_NOT_FOUND
    assert "not found" in error.message.lower()


@pytest.mark.asyncio
async def test_add_user_success(user_service, mocker):
    """Test successfully adding a new user through service."""
    # Prepare test data
    user_data = UserCreate(
        email="new.user@example.com",
        first_name="New",
        last_name="User",
        password="password123",
    )

    # Prepare mock result
    mock_user = User(
        id="new-id",
        email="new.user@example.com",
        first_name="New",
        last_name="User",
        password="hashed_password",
    )

    # Setup mock behavior
    mocker.patch.object(user_service.user_repo, "add_user", return_value=mock_user)

    # Execute service method
    result = await user_service.add_user(user_data)

    # Verify results
    assert result == mock_user
    assert result.email == user_data.email
    assert result.first_name == user_data.first_name
    assert result.last_name == user_data.last_name
    user_service.user_repo.add_user.assert_called_once_with(user_data)


@pytest.mark.asyncio
async def test_add_user_duplicate_email(user_service, mocker):
    """Test handling duplicate email error when adding a user."""
    # Prepare test data
    user_data = UserCreate(
        email="existing@example.com",
        first_name="Existing",
        last_name="User",
        password="password123",
    )

    # Setup mock behavior
    mocker.patch.object(
        user_service.user_repo,
        "add_user",
        side_effect=DuplicateUserError(
            message="User with email 'existing@example.com' already exists"
        ),
    )

    # Execute and verify
    with pytest.raises(DuplicateUserError) as exc_info:
        await user_service.add_user(user_data)

    error = exc_info.value
    assert error.status_code == status.HTTP_409_CONFLICT
    assert "already exists" in error.message


@pytest.mark.asyncio
async def test_update_user_success(user_service, mocker):
    """Test successfully updating a user through service."""
    # Prepare test data
    user_update = UserUpdate(
        email="updated.email@example.com",
        first_name="Updated",
        last_name="Name",
    )

    # Prepare mock result
    mock_updated_user = User(
        id="1",
        email="updated.email@example.com",
        first_name="Updated",
        last_name="Name",
        password="hashed_password",
    )

    # Setup mock behavior
    mocker.patch.object(
        user_service.user_repo, "update_user", return_value=mock_updated_user
    )

    # Execute service method
    result = await user_service.update_user("1", user_update)

    # Verify results
    assert result == mock_updated_user
    assert result.email == user_update.email
    assert result.first_name == user_update.first_name
    assert result.last_name == user_update.last_name
    user_service.user_repo.update_user.assert_called_once_with("1", user_update)


@pytest.mark.asyncio
async def test_update_user_not_found(user_service, mocker):
    """Test handling user not found error when updating a user."""
    # Prepare test data
    user_update = UserUpdate(
        email="updated.email@example.com",
        first_name="Updated",
        last_name="Name",
    )

    # Setup mock behavior
    mocker.patch.object(
        user_service.user_repo,
        "update_user",
        side_effect=UserNotFoundError(
            message="User with ID 'non-existent-id' not found"
        ),
    )

    # Execute and verify
    with pytest.raises(UserNotFoundError) as exc_info:
        await user_service.update_user("non-existent-id", user_update)

    error = exc_info.value
    assert error.status_code == status.HTTP_404_NOT_FOUND
    assert "not found" in error.message.lower()


@pytest.mark.asyncio
async def test_delete_user_success(user_service, mocker):
    """Test successfully deleting a user through service."""
    # Setup mock behavior
    mocker.patch.object(user_service.user_repo, "delete_user", return_value=None)

    # Execute service method
    await user_service.delete_user("1")

    # Verify results
    user_service.user_repo.delete_user.assert_called_once_with("1")


@pytest.mark.asyncio
async def test_delete_user_not_found(user_service, mocker):
    """Test handling user not found error when deleting a user."""
    # Setup mock behavior
    mocker.patch.object(
        user_service.user_repo,
        "delete_user",
        side_effect=UserNotFoundError(
            message="User with ID 'non-existent-id' not found"
        ),
    )

    # Execute and verify
    with pytest.raises(UserNotFoundError) as exc_info:
        await user_service.delete_user("non-existent-id")

    error = exc_info.value
    assert error.status_code == status.HTTP_404_NOT_FOUND
    assert "not found" in error.message.lower()
