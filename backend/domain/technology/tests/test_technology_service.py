"""Tests for the technology service."""

import pytest
from database.models import Technology
from domain.technology.exceptions import (
    TechnologyDatabaseError,
    TechnologyNotFoundError,
)
from domain.technology.technology_models import Technology_Create, TechnologyWithCount
from domain.technology.technology_repo import TechnologyRepo
from domain.technology.technology_service import TechnologyService
from enums import Language
from fastapi import status


@pytest.fixture
def mock_technology_repo(mocker):
    """Create a mock technology repository."""
    return mocker.Mock(spec=TechnologyRepo)


@pytest.fixture
def technology_service(mock_technology_repo):
    """Create a TechnologyService with a mocked repository."""
    return TechnologyService(mock_technology_repo)


def test_get_technologies_success(technology_service, mock_technology_repo):
    """Test successful retrieval of technologies through service."""
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

    # Setup mock behavior
    mock_technology_repo.get_technologies.return_value = mock_technologies

    # Execute service method
    result = technology_service.get_technologies()

    # Verify results
    assert result == mock_technologies
    mock_technology_repo.get_technologies.assert_called_once_with(language=None)


def test_get_technologies_with_filter(technology_service, mock_technology_repo):
    """Test getting technologies with language filter."""
    # Setup mock behavior
    mock_technology_repo.get_technologies.return_value = []

    # Execute service method with filter
    result = technology_service.get_technologies(language=Language.PYTHON)

    # Verify repository was called with correct filter
    mock_technology_repo.get_technologies.assert_called_once_with(
        language=Language.PYTHON
    )
    assert isinstance(result, list)


def test_get_technologies_handles_error(technology_service, mock_technology_repo):
    """Test error handling when getting technologies."""
    # Setup mock to raise error
    mock_technology_repo.get_technologies.side_effect = TechnologyDatabaseError(
        "Database error"
    )

    # Verify error is propagated
    with pytest.raises(TechnologyDatabaseError) as exc_info:
        technology_service.get_technologies()

    assert "Database error" in str(exc_info.value)


def test_add_technology_success(technology_service, mock_technology_repo):
    """Test successful technology creation."""
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

    # Setup mock behavior
    mock_technology_repo.add_technology.return_value = mock_result

    # Execute service method
    result = technology_service.add_technology(new_tech)

    # Verify results
    assert result == mock_result
    mock_technology_repo.add_technology.assert_called_once_with(new_tech)


def test_add_technology_handles_error(technology_service, mock_technology_repo):
    """Test error handling during technology creation."""
    # Setup mock to raise error
    mock_technology_repo.add_technology.side_effect = TechnologyDatabaseError(
        "Duplicate name"
    )

    # Prepare test data
    new_tech = Technology_Create(name="Existing")

    # Verify error is propagated
    with pytest.raises(TechnologyDatabaseError) as exc_info:
        technology_service.add_technology(new_tech)

    assert "Duplicate name" in str(exc_info.value)


def test_delete_technology_success(technology_service, mock_technology_repo):
    """Test successful technology deletion."""
    # Execute service method
    technology_service.delete_technology("1")

    # Verify repository was called
    mock_technology_repo.delete_technology.assert_called_once_with("1")


def test_delete_technology_not_found(technology_service, mock_technology_repo):
    """Test deletion of non-existent technology."""
    # Setup mock to raise not found error
    mock_technology_repo.delete_technology.side_effect = TechnologyNotFoundError()

    # Verify error is propagated
    with pytest.raises(TechnologyNotFoundError):
        technology_service.delete_technology("non-existent-id")


def test_delete_technology_with_entries(technology_service, mock_technology_repo):
    """Test deletion of technology with journal entries."""
    # Setup mock to raise error
    mock_technology_repo.delete_technology.side_effect = TechnologyDatabaseError(
        "Cannot delete: has entries",
        status_code=status.HTTP_400_BAD_REQUEST,
    )

    # Verify error is propagated with correct status
    with pytest.raises(TechnologyDatabaseError) as exc_info:
        technology_service.delete_technology("1")

    assert exc_info.value.status_code == status.HTTP_400_BAD_REQUEST
    assert "Cannot delete: has entries" in str(exc_info.value)
