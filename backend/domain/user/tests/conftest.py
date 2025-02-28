import pytest
from database.models import User
from domain.user.user_repo import UserRepo
from domain.user.user_service import UserService

# flake8: noqa: F401
from tests.conftest import *


@pytest.fixture
def user_repo(db_session) -> UserRepo:
    """Create a UserRepo instance for testing."""
    return UserRepo(db_session)


@pytest.fixture
def user_service(user_repo: UserRepo) -> UserService:
    """Create a UserService instance for testing."""
    return UserService(user_repo=user_repo)


@pytest_asyncio.fixture(name="sample_users")
async def sample_users() -> list[User]:
    """Create sample users for testing."""
    return [
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
