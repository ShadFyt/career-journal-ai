"""Tests for the technology repository."""

import pytest
from sqlalchemy.exc import SQLAlchemyError
from domain.technology.technology_repo import TechnologyRepo
from domain.technology.exceptions import (
    TechnologyDatabaseError,
    TechnologyNotFoundError,
)
from domain.technology.technology_models import TechnologyWithCount
from database.models import Technology, JournalEntryTechnologyLink
from enums import Language
from fastapi import status


@pytest.fixture
def sample_technologies(db_session):
    """Create sample technologies for testing."""
    technologies = [
        Technology(
            id="1",
            name="Python",
            description="Programming language",
            language=Language.PYTHON,
        ),
        Technology(
            id="2",
            name="JavaScript",
            description="Web language",
            language=Language.JAVASCRIPT,
        ),
        Technology(
            id="3", name="React", description="UI library", language=Language.JAVASCRIPT
        ),
    ]
    for tech in technologies:
        db_session.add(tech)
    db_session.commit()
    return technologies


@pytest.fixture
def sample_tech_usage(db_session, sample_technologies):
    """Create sample technology usage records."""
    usages = [
        JournalEntryTechnologyLink(
            journal_entry_id="entry1", technology_id=sample_technologies[0].id
        ),
        JournalEntryTechnologyLink(
            journal_entry_id="entry2", technology_id=sample_technologies[0].id
        ),
        JournalEntryTechnologyLink(
            journal_entry_id="entry1", technology_id=sample_technologies[1].id
        ),
    ]
    for usage in usages:
        db_session.add(usage)
    db_session.commit()
    return usages


def test_get_technologies_returns_list_with_counts(
    technology_repo: TechnologyRepo, sample_technologies, sample_tech_usage
):
    """Test that get_technologies returns all technologies with correct usage counts."""
    technologies = technology_repo.get_technologies()

    assert len(technologies) == 3
    assert all(isinstance(tech, TechnologyWithCount) for tech in technologies)

    # Python should have 2 usages
    python_tech = next(t for t in technologies if t.name == "Python")
    assert python_tech.usage_count == 2

    # JavaScript should have 1 usage
    js_tech = next(t for t in technologies if t.name == "JavaScript")
    assert js_tech.usage_count == 1

    # React should have 0 usages
    react_tech = next(t for t in technologies if t.name == "React")
    assert react_tech.usage_count == 0


def test_get_technologies_filters_by_language(
    technology_repo: TechnologyRepo, sample_technologies
):
    """Test that get_technologies correctly filters by programming language."""
    # Get only JavaScript technologies
    js_techs = technology_repo.get_technologies(language=Language.JAVASCRIPT)
    assert len(js_techs) == 2
    assert all(tech.language == Language.JAVASCRIPT for tech in js_techs)

    # Get only Python technologies
    py_techs = technology_repo.get_technologies(language=Language.PYTHON)
    assert len(py_techs) == 1
    assert all(tech.language == Language.PYTHON for tech in py_techs)


def test_get_technologies_empty_database(technology_repo: TechnologyRepo):
    """Test that get_technologies returns empty list for empty database."""
    technologies = technology_repo.get_technologies()
    assert isinstance(technologies, list)
    assert len(technologies) == 0


def test_get_technologies_handles_database_error(
    technology_repo: TechnologyRepo, mocker
):
    """Test that get_technologies properly handles database errors."""
    # Mock the session to raise an error
    mocker.patch.object(
        technology_repo.session, "exec", side_effect=SQLAlchemyError("Database error")
    )

    with pytest.raises(TechnologyDatabaseError) as exc_info:
        technology_repo.get_technologies()

    assert "Failed to fetch technologies" in str(exc_info.value)


def test_get_technology_success(technology_repo: TechnologyRepo, sample_technologies):
    """Test successfully getting a technology by ID."""
    # Get the first sample technology
    tech = technology_repo.get_technology(sample_technologies[0].id)

    # Verify the returned technology
    assert tech is not None
    assert tech.id == sample_technologies[0].id
    assert tech.name == sample_technologies[0].name
    assert tech.description == sample_technologies[0].description
    assert tech.language == sample_technologies[0].language


def test_get_technology_not_found(technology_repo: TechnologyRepo):
    """Test getting a non-existent technology raises correct error."""
    with pytest.raises(TechnologyNotFoundError) as exc_info:
        technology_repo.get_technology("non-existent-id")
    assert exc_info.value.status_code == status.HTTP_404_NOT_FOUND


def test_get_technology_database_error(technology_repo: TechnologyRepo, mocker):
    """Test database error handling when getting a technology."""
    # Mock the session to raise a database error
    mocker.patch.object(
        technology_repo.session, "get", side_effect=SQLAlchemyError("Database error")
    )

    with pytest.raises(TechnologyDatabaseError) as exc_info:
        technology_repo.get_technology("any-id")
    assert "Failed to fetch technology" in str(exc_info.value)
