import pytest
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
