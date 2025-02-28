"""Tests for the user repository."""

import pytest
import pytest_asyncio
from database.models import User
from domain.user.user_exceptions import (
    DuplicateUserError,
    UserDatabaseError,
    UserNotFoundError,
)
from domain.user.user_repo import UserRepo
from domain.user.user_schema import UserCreate, UserUpdate
from fastapi import status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm.session import Session as SessionDep
from conftest import sample_users


@pytest_asyncio.fixture
async def db_sample_users(db_session: SessionDep, sample_users) -> list[User]:
    """Add sample users to the database for testing."""
    for user in sample_users:
        db_session.add(user)
        await db_session.commit()
    return sample_users


@pytest.mark.asyncio
async def test_get_users_success(user_repo: UserRepo, db_sample_users):
    """Test successfully getting all users."""
    users = await user_repo.get_users()
    assert users is not None
    assert len(users) >= 2
    # Check if our sample users are in the result
    user_emails = [user.email for user in users]
    assert db_sample_users[0].email in user_emails
    assert db_sample_users[1].email in user_emails


@pytest.mark.asyncio
async def test_get_users_database_error(user_repo: UserRepo, mocker):
    """Test handling of database errors when getting users."""
    mocker.patch.object(
        user_repo.session, "exec", side_effect=SQLAlchemyError("Database error")
    )
    with pytest.raises(UserDatabaseError) as exc_info:
        await user_repo.get_users()
    assert "Failed to fetch users" in str(exc_info.value)


@pytest.mark.asyncio
async def test_get_user_success(user_repo: UserRepo, db_sample_users):
    """Test successfully getting a user by ID."""
    user = await user_repo.get_user(db_sample_users[0].id)
    assert user is not None
    assert user.id == db_sample_users[0].id
    assert user.email == db_sample_users[0].email
    assert user.first_name == db_sample_users[0].first_name
    assert user.last_name == db_sample_users[0].last_name


@pytest.mark.asyncio
async def test_get_user_not_found(user_repo: UserRepo):
    """Test getting a non-existent user raises correct error."""
    with pytest.raises(UserNotFoundError) as exc_info:
        await user_repo.get_user("non-existent-id")

    error = exc_info.value
    assert error.status_code == status.HTTP_404_NOT_FOUND
    assert "not found" in str(error.message).lower()


@pytest.mark.asyncio
async def test_add_user_success(user_repo: UserRepo):
    """Test successfully adding a new user."""
    new_user = UserCreate(
        email="new.user@example.com",
        first_name="New",
        last_name="User",
        password="password123",
    )
    result = await user_repo.add_user(new_user)
    assert result is not None
    assert result.email == new_user.email
    assert result.first_name == new_user.first_name
    assert result.last_name == new_user.last_name
    assert isinstance(result, User)


@pytest.mark.asyncio
async def test_add_user_duplicate_email(user_repo: UserRepo, db_sample_users):
    """Test adding a user with an existing email raises correct error."""
    duplicate_user = UserCreate(
        email=db_sample_users[0].email,  # Using existing email
        first_name="Duplicate",
        last_name="User",
        password="password123",
    )
    with pytest.raises(DuplicateUserError) as exc_info:
        await user_repo.add_user(duplicate_user)
    assert "already exists" in str(exc_info.value)


@pytest.mark.asyncio
async def test_add_user_database_error(user_repo: UserRepo, mocker):
    """Test handling of database errors when adding user."""
    mocker.patch.object(
        user_repo.session, "add", side_effect=SQLAlchemyError("Database error")
    )
    with pytest.raises(UserDatabaseError) as exc_info:
        await user_repo.add_user(
            UserCreate(
                email="test@example.com",
                first_name="Test",
                last_name="User",
                password="password123",
            )
        )
    assert "Failed to add user" in str(exc_info.value)


@pytest.mark.asyncio
async def test_update_user_success(user_repo: UserRepo, db_sample_users):
    """Test successfully updating a user."""
    updated_data = UserUpdate(
        email="updated.email@example.com",
        first_name="Updated",
        last_name="Name",
    )
    result = await user_repo.update_user(db_sample_users[0].id, updated_data)
    assert result is not None
    assert result.email == updated_data.email
    assert result.first_name == updated_data.first_name
    assert result.last_name == updated_data.last_name
    # Password should remain unchanged
    assert result.password == db_sample_users[0].password


@pytest.mark.asyncio
async def test_update_user_not_found(user_repo: UserRepo):
    """Test updating a non-existent user raises correct error."""
    with pytest.raises(UserNotFoundError) as exc_info:
        await user_repo.update_user(
            "non-existent-id",
            UserUpdate(
                email="updated@example.com",
                first_name="Updated",
                last_name="User",
            ),
        )
    assert exc_info.value.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio
async def test_update_user_database_error(user_repo: UserRepo, db_sample_users, mocker):
    """Test handling of database errors when updating user."""
    # Mock the _save_user method to raise an exception
    mocker.patch.object(
        user_repo, "_save_user", side_effect=SQLAlchemyError("Database error")
    )
    with pytest.raises(UserDatabaseError) as exc_info:
        await user_repo.update_user(
            db_sample_users[0].id,
            UserUpdate(
                email="updated@example.com",
                first_name="Updated",
                last_name="User",
            ),
        )
    assert "Failed to update user" in str(exc_info.value)


@pytest.mark.asyncio
async def test_delete_user_success(user_repo: UserRepo, db_sample_users):
    """Test successfully deleting a user."""
    # First verify the user exists
    user = await user_repo.get_user(db_sample_users[0].id)
    assert user is not None

    # Delete the user
    await user_repo.delete_user(db_sample_users[0].id)

    # Verify the user no longer exists
    with pytest.raises(UserNotFoundError):
        await user_repo.get_user(db_sample_users[0].id)


@pytest.mark.asyncio
async def test_delete_user_not_found(user_repo: UserRepo):
    """Test deleting a non-existent user raises correct error."""
    with pytest.raises(UserNotFoundError) as exc_info:
        await user_repo.delete_user("non-existent-id")
    assert exc_info.value.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio
async def test_delete_user_database_error(user_repo: UserRepo, db_sample_users, mocker):
    """Test handling of database errors when deleting user."""
    # Mock the session.delete method to raise an exception
    mocker.patch.object(
        user_repo.session, "delete", side_effect=SQLAlchemyError("Database error")
    )
    with pytest.raises(UserDatabaseError) as exc_info:
        await user_repo.delete_user(db_sample_users[0].id)
    assert "Failed to delete user" in str(exc_info.value)


@pytest.mark.asyncio
async def test_save_user_success(user_repo: UserRepo):
    """Test successfully saving a user."""
    # Create a new user object
    new_user = User(
        email="save.test@example.com",
        first_name="Save",
        last_name="Test",
        password="password123",
    )

    # Save the user
    result = await user_repo._save_user(new_user)

    # Verify the user was saved correctly
    assert result is not None
    assert result.email == new_user.email
    assert result.first_name == new_user.first_name
    assert result.last_name == new_user.last_name
    assert result.id is not None  # ID should be generated
