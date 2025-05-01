"""Tests for the technology repository."""

import pytest
import pytest_asyncio
from database.models import JournalEntry, JournalEntryTechnologyLink, Technology
from domain.technology.technology_exceptions import (
    ErrorCode,
    TechnologyDatabaseError,
    TechnologyNotFoundError,
)
from domain.technology.technology_repo import TechnologyRepo
from domain.technology.technology_schema import TechnologyCreate, TechnologyWithCount
from enums import Language
from fastapi import status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm.session import Session as SessionDep

mock_user_id = "123"


@pytest_asyncio.fixture
async def sample_technologies(db_session: SessionDep) -> list[Technology]:
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
        await db_session.commit()
    return technologies


@pytest_asyncio.fixture
async def sample_journal_entries(db_session):
    """Create sample journal entries for testing."""
    entries = [
        JournalEntry(
            id="entry1",
            content="Test entry 1",
            project_id="project1",
            user_id=mock_user_id,
        ),
        JournalEntry(
            id="entry2",
            content="Test entry 2",
            project_id="project1",
            user_id=mock_user_id,
        ),
    ]
    for entry in entries:
        db_session.add(entry)
    await db_session.commit()
    return entries


@pytest_asyncio.fixture
async def sample_tech_usage(db_session, sample_technologies, sample_journal_entries):
    """Create sample technology usage records."""
    usages = [
        JournalEntryTechnologyLink(
            journal_entry_id=sample_journal_entries[0].id,
            technology_id=sample_technologies[0].id,
        ),
        JournalEntryTechnologyLink(
            journal_entry_id=sample_journal_entries[1].id,
            technology_id=sample_technologies[0].id,
        ),
        JournalEntryTechnologyLink(
            journal_entry_id=sample_journal_entries[0].id,
            technology_id=sample_technologies[1].id,
        ),
    ]
    for usage in usages:
        db_session.add(usage)
    await db_session.commit()
    return usages


@pytest.mark.asyncio
async def test_get_technologies_returns_list_with_counts(
    technology_repo: TechnologyRepo, sample_technologies, sample_tech_usage
):
    """Test that get_technologies returns all technologies with correct usage counts."""
    technologies = await technology_repo.get_technologies()

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


@pytest.mark.asyncio
async def test_get_technologies_filters_by_language(
    technology_repo: TechnologyRepo, sample_technologies
):
    """Test that get_technologies correctly filters by programming language."""
    # Get only JavaScript technologies
    js_techs = await technology_repo.get_technologies(language=Language.JAVASCRIPT)
    assert len(js_techs) == 2
    assert all(tech.language == Language.JAVASCRIPT for tech in js_techs)

    # Get only Python technologies
    py_techs = await technology_repo.get_technologies(language=Language.PYTHON)
    assert len(py_techs) == 1
    assert all(tech.language == Language.PYTHON for tech in py_techs)


@pytest.mark.asyncio
async def test_get_technologies_empty_database(technology_repo: TechnologyRepo):
    """Test that get_technologies returns empty list for empty database."""
    technologies = await technology_repo.get_technologies()
    assert isinstance(technologies, list)
    assert len(technologies) == 0


@pytest.mark.asyncio
async def test_get_technologies_handles_database_error(
    technology_repo: TechnologyRepo, mocker
):
    """Test that get_technologies properly handles database errors."""
    # Mock the session to raise an error
    mocker.patch.object(
        technology_repo.session, "exec", side_effect=SQLAlchemyError("Database error")
    )

    with pytest.raises(TechnologyDatabaseError) as exc_info:
        await technology_repo.get_technologies()

    assert "Failed to fetch technologies" in str(exc_info.value)


@pytest.mark.asyncio
async def test_get_technology_success(
    technology_repo: TechnologyRepo, sample_technologies
):
    """Test successfully getting a technology by ID."""
    # Get the first sample technology
    tech = await technology_repo.get_technology(sample_technologies[0].id)

    # Verify the returned technology
    assert tech is not None
    assert tech.id == sample_technologies[0].id
    assert tech.name == sample_technologies[0].name
    assert tech.description == sample_technologies[0].description
    assert tech.language == sample_technologies[0].language


@pytest.mark.asyncio
async def test_get_technology_not_found(technology_repo: TechnologyRepo):
    """Test getting a non-existent technology raises correct error."""
    with pytest.raises(TechnologyNotFoundError) as exc_info:
        await technology_repo.get_technology("non-existent-id")
    assert exc_info.value.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio
async def test_get_technology_database_error(technology_repo: TechnologyRepo, mocker):
    """Test database error handling when getting a technology."""
    # Mock the session to raise a database error
    mocker.patch.object(
        technology_repo.session, "exec", side_effect=SQLAlchemyError("Database error")
    )

    with pytest.raises(TechnologyDatabaseError) as exc_info:
        await technology_repo.get_technology("any-id")
    assert "Failed to fetch technology" in str(exc_info.value)


@pytest.mark.asyncio
async def test_add_technology_success(technology_repo: TechnologyRepo):
    """Test successfully adding a new technology."""
    new_tech = TechnologyCreate(
        name="TypeScript",
        description="JavaScript with types",
        language=Language.JAVASCRIPT,
    )

    # Add the technology
    result = await technology_repo.add_technology(new_tech)

    # Verify the result
    assert result is not None
    assert result.name == new_tech.name
    assert result.description == new_tech.description
    assert result.language == new_tech.language
    assert isinstance(result.id, str)  # Should have generated UUID


@pytest.mark.asyncio
async def test_add_technology_duplicate_name(
    technology_repo: TechnologyRepo, sample_technologies
):
    """Test that adding a technology with duplicate name raises correct error."""
    duplicate_tech = TechnologyCreate(
        name="Python",  # Same name as in sample_technologies
        description="Different description",
        language=Language.PYTHON,
    )

    with pytest.raises(TechnologyDatabaseError) as exc_info:
        await technology_repo.add_technology(duplicate_tech)

    error = exc_info.value
    assert error.message == "Technology with this name already exists"
    assert error.code == ErrorCode.DUPLICATE_TECHNOLOGY
    assert error.params["name"] == "Python"
    assert error.status_code == status.HTTP_409_CONFLICT


@pytest.mark.asyncio
async def test_add_technology_database_error(technology_repo: TechnologyRepo, mocker):
    """Test handling of database errors when adding technology."""
    # Mock the session to raise a database error
    mocker.patch.object(
        technology_repo.session,
        "add",
        side_effect=SQLAlchemyError("Database error"),
    )

    new_tech = TechnologyCreate(
        name="NewTech",
        description="Test tech",
        language=Language.PYTHON,
    )

    with pytest.raises(TechnologyDatabaseError) as exc_info:
        await technology_repo.add_technology(new_tech)

    assert "Failed to add technology" in str(exc_info.value)


@pytest.mark.asyncio
async def test_add_technology_with_minimal_data(technology_repo: TechnologyRepo):
    """Test adding a technology with only required fields."""
    minimal_tech = TechnologyCreate(name="MinimalTech")

    result = await technology_repo.add_technology(minimal_tech)

    assert result is not None
    assert result.name == "MinimalTech"
    assert result.description is None
    assert result.language is None
    assert isinstance(result.id, str)


@pytest.mark.asyncio
async def test_delete_technology_success(
    technology_repo: TechnologyRepo, sample_technologies
):
    """Test successfully deleting a technology."""
    # Get a technology without journal entries (React from sample data)
    tech_to_delete = sample_technologies[2]  # React technology

    # Delete the technology
    await technology_repo.delete_technology(tech_to_delete.id)

    # Verify technology is deleted
    with pytest.raises(TechnologyNotFoundError):
        await technology_repo.get_technology(tech_to_delete.id)


@pytest.mark.asyncio
async def test_delete_technology_with_journal_entries(
    technology_repo: TechnologyRepo,
    sample_technologies,
    sample_tech_usage,
):
    """Test that deleting a technology with journal entries raises correct error."""
    # Try to delete Python which has journal entries in sample_tech_usage
    tech_with_entries = sample_technologies[0]  # Python technology

    with pytest.raises(TechnologyDatabaseError) as exc_info:
        await technology_repo.delete_technology(tech_with_entries.id)

    error = exc_info.value

    assert (
        error.message
        == "Cannot delete technology that is referenced by journal entries"
    )
    assert error.status_code == status.HTTP_409_CONFLICT
    assert error.code == ErrorCode.INVALID_OPERATION

    # Verify technology still exists
    tech = await technology_repo.get_technology(tech_with_entries.id)
    assert tech is not None
    assert tech.id == tech_with_entries.id


@pytest.mark.asyncio
async def test_delete_technology_not_found(technology_repo: TechnologyRepo):
    """Test deleting a non-existent technology raises correct error."""
    with pytest.raises(TechnologyNotFoundError):
        await technology_repo.delete_technology("non-existent-id")


@pytest.mark.asyncio
async def test_delete_technology_database_error(
    technology_repo: TechnologyRepo, sample_technologies, mocker
):
    """Test handling of database errors when deleting technology."""
    # Mock the session delete to raise an error
    mocker.patch.object(
        technology_repo.session,
        "delete",
        side_effect=SQLAlchemyError("Database error"),
    )

    with pytest.raises(TechnologyDatabaseError) as exc_info:
        await technology_repo.delete_technology(
            sample_technologies[2].id
        )  # React technology

    assert "Failed to delete technology" in str(exc_info.value)
