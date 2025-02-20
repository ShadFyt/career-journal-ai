"""Test fixtures for technology domain tests."""

import pytest
from domain.technology.technology_repo import TechnologyRepo
from domain.technology.technology_service import TechnologyService

# flake8: noqa: F401
from tests.conftest import *


@pytest.fixture
def technology_repo(db_session) -> TechnologyRepo:
    """Create a TechnologyRepo instance for testing."""
    return TechnologyRepo(db_session)


@pytest.fixture
def technology_service(technology_repo: TechnologyRepo) -> TechnologyService:
    """Create a TechnologyService instance for testing."""
    return TechnologyService(technology_repo)
