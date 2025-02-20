import pytest
from domain.project.project_repo import ProjectRepo
from domain.project.project_service import ProjectService

# flake8: noqa: F401
from tests.conftest import *


@pytest.fixture
def project_repo(db_session) -> ProjectRepo:
    """Create a ProjectRepo instance for testing."""
    return ProjectRepo(db_session)


@pytest.fixture
def project_service(project_repo: ProjectRepo) -> ProjectService:
    """Create a ProjectService instance for testing."""
    return ProjectService(project_repo)
