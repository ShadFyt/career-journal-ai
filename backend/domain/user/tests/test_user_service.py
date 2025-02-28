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
async def test_get_users_success(user_service, mocker, sample_users):
    """Test successfully retrieving all users through service."""
    # Setup mock behavior
    mocker.patch.object(user_service.user_repo, "get_users", return_value=sample_users)

    # Execute service method
    result = await user_service.get_users()

    # Verify results
    assert result == sample_users
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
async def test_get_user_success(user_service, mocker, sample_users):
    """Test successfully retrieving a user by ID through service."""
    # Setup mock behavior
    mocker.patch.object(
        user_service.user_repo, "get_user", return_value=sample_users[0]
    )

    # Execute service method
    result = await user_service.get_user(sample_users[0].id)

    # Verify results
    assert result == sample_users[0]
    assert result.id == sample_users[0].id
    assert result.email == sample_users[0].email
    user_service.user_repo.get_user.assert_called_once_with(sample_users[0].id)


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
async def test_add_user_success(user_service, mocker, sample_users):
    """Test successfully adding a new user through service."""
    # Prepare test data
    user_data = UserCreate(
        email="new.user@example.com",
        first_name="New",
        last_name="User",
        password="password123",
    )

    # Create a new user based on the input data
    new_user = User(
        id="new-id",
        email=user_data.email,
        first_name=user_data.first_name,
        last_name=user_data.last_name,
        password="hashed_" + user_data.password,  # Simulate hashing
    )

    # Setup mock behavior
    mocker.patch.object(user_service.user_repo, "add_user", return_value=new_user)

    # Execute service method
    result = await user_service.add_user(user_data)

    # Verify results
    assert result == new_user
    assert result.id == "new-id"
    assert result.email == user_data.email
    assert result.first_name == user_data.first_name
    assert result.last_name == user_data.last_name
    # Password should be hashed
    assert result.password != user_data.password
    assert result.password == "hashed_" + user_data.password
    user_service.user_repo.add_user.assert_called_once_with(user_data)


@pytest.mark.asyncio
async def test_add_user_duplicate_email(user_service, mocker, sample_users):
    """Test handling duplicate email error when adding a user."""
    # Prepare test data
    user_data = UserCreate(
        email=sample_users[0].email,  # Use existing email from sample_users
        first_name="Duplicate",
        last_name="User",
        password="password123",
    )

    # Setup mock behavior
    mocker.patch.object(
        user_service.user_repo,
        "add_user",
        side_effect=DuplicateUserError(
            message=f"User with email '{user_data.email}' already exists"
        ),
    )

    # Execute and verify
    with pytest.raises(DuplicateUserError) as exc_info:
        await user_service.add_user(user_data)

    error = exc_info.value
    assert error.status_code == status.HTTP_409_CONFLICT
    assert f"User with email '{user_data.email}' already exists" in error.message


@pytest.mark.asyncio
async def test_update_user_success(user_service, mocker, sample_users):
    """Test successfully updating a user through service."""
    # Prepare test data
    user_update = UserUpdate(
        email="updated.email@example.com",
        first_name="Updated",
        last_name="Name",
    )

    # Create an updated user based on the sample user and update data
    updated_user = User(
        id=sample_users[0].id,
        email=user_update.email,
        first_name=user_update.first_name,
        last_name=user_update.last_name,
        password=sample_users[0].password,  # Password should remain unchanged
    )

    # Setup mock behavior
    mocker.patch.object(
        user_service.user_repo, "update_user", return_value=updated_user
    )

    # Execute service method
    result = await user_service.update_user(sample_users[0].id, user_update)

    # Verify results
    assert result == updated_user
    assert result.id == sample_users[0].id
    assert result.email == user_update.email
    assert result.first_name == user_update.first_name
    assert result.last_name == user_update.last_name
    # Password should remain unchanged
    assert result.password == sample_users[0].password
    user_service.user_repo.update_user.assert_called_once_with(
        sample_users[0].id, user_update
    )


@pytest.mark.asyncio
async def test_update_user_not_found(user_service, mocker, sample_users):
    """Test handling user not found error when updating a user."""
    # Prepare test data
    user_id = "non-existent-id"
    user_update = UserUpdate(
        email="updated.email@example.com",
        first_name="Updated",
        last_name="Name",
    )

    # Setup mock behavior
    mocker.patch.object(
        user_service.user_repo,
        "update_user",
        side_effect=UserNotFoundError(message=f"User with ID '{user_id}' not found"),
    )

    # Execute and verify
    with pytest.raises(UserNotFoundError) as exc_info:
        await user_service.update_user(user_id, user_update)

    error = exc_info.value
    assert error.status_code == status.HTTP_404_NOT_FOUND
    assert f"User with ID '{user_id}' not found" in error.message


@pytest.mark.asyncio
async def test_delete_user_success(user_service, mocker, sample_users):
    """Test successfully deleting a user through service."""
    # Setup mock behavior
    mocker.patch.object(user_service.user_repo, "delete_user", return_value=None)

    # Execute service method
    await user_service.delete_user(sample_users[0].id)

    # Verify the repository method was called with the correct ID
    user_service.user_repo.delete_user.assert_called_once_with(sample_users[0].id)


@pytest.mark.asyncio
async def test_delete_user_not_found(user_service, mocker, sample_users):
    """Test handling user not found error when deleting a user."""
    # Prepare test data
    user_id = "non-existent-id"

    # Setup mock behavior
    mocker.patch.object(
        user_service.user_repo,
        "delete_user",
        side_effect=UserNotFoundError(message=f"User with ID '{user_id}' not found"),
    )

    # Execute and verify
    with pytest.raises(UserNotFoundError) as exc_info:
        await user_service.delete_user(user_id)

    error = exc_info.value
    assert error.status_code == status.HTTP_404_NOT_FOUND
    assert f"User with ID '{user_id}' not found" in error.message
