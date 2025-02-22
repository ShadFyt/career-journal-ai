"""Tests for the journal entry repository."""

from datetime import datetime

import pytest
import pytest_asyncio
from database.models import JournalEntry, Technology
from domain.journal_entry.journal_entry_exceptions import (
    JournalEntryDatabaseError,
    JournalEntryNotFoundError,
)
from domain.journal_entry.journal_entry_repo import JournalEntryRepo
from domain.journal_entry.journal_entry_schema import (
    JournalEntryCreate,
    JournalEntryUpdate,
)
from fastapi import status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm.session import Session as SessionDep


@pytest_asyncio.fixture
async def sample_journal_entries(db_session: SessionDep) -> list[JournalEntry]:
    """Create sample journal entries for testing."""
    entries = [
        JournalEntry(
            id="entry1",
            content="Test entry 1",
            date=datetime(2025, 1, 1),
            project_id="project1",
        ),
        JournalEntry(
            id="entry2",
            content="Test entry 2",
            date=datetime(2025, 1, 2),
            project_id="project1",
        ),
    ]
    for entry in entries:
        db_session.add(entry)
        await db_session.commit()
    return entries


@pytest_asyncio.fixture
async def sample_technologies(db_session: SessionDep) -> list[Technology]:
    """Create sample technologies for testing."""
    technologies = [
        Technology(
            id="tech1",
            name="Python",
            description="Programming language",
        ),
        Technology(
            id="tech2",
            name="JavaScript",
            description="Web language",
        ),
    ]
    for tech in technologies:
        db_session.add(tech)
        await db_session.commit()
    return technologies


@pytest.mark.asyncio
async def test_get_journal_entries_success(
    journal_entry_repo: JournalEntryRepo, sample_journal_entries
):
    """Test that get_journal_entries returns all entries sorted by date."""
    entries = await journal_entry_repo.get_journal_entries()
    assert len(entries) == 2
    assert entries[0].date > entries[1].date  # Verify sorting


@pytest.mark.asyncio
async def test_get_journal_entries_empty_database(journal_entry_repo: JournalEntryRepo):
    """Test that get_journal_entries returns empty list for empty database."""
    entries = await journal_entry_repo.get_journal_entries()
    assert isinstance(entries, list)
    assert len(entries) == 0


@pytest.mark.asyncio
async def test_get_journal_entries_database_error(
    journal_entry_repo: JournalEntryRepo, mocker
):
    """Test that get_journal_entries handles database errors."""
    mocker.patch.object(
        journal_entry_repo.session,
        "exec",
        side_effect=SQLAlchemyError("Database error"),
    )
    with pytest.raises(JournalEntryDatabaseError):
        await journal_entry_repo.get_journal_entries()


@pytest.mark.asyncio
async def test_get_journal_entry_success(
    journal_entry_repo: JournalEntryRepo, sample_journal_entries
):
    """Test successfully getting a journal entry by ID."""
    entry = await journal_entry_repo.get_journal_entry(sample_journal_entries[0].id)
    assert entry.id == sample_journal_entries[0].id
    assert entry.content == sample_journal_entries[0].content


@pytest.mark.asyncio
async def test_get_journal_entry_not_found(
    journal_entry_repo: JournalEntryRepo, mocker
):
    """Test getting a non-existent journal entry raises correct error."""
    # Mock session.get to return None, simulating entry not found
    # mocker.patch.object(journal_entry_repo.session, "get", return_value=None)

    with pytest.raises(JournalEntryNotFoundError) as exc_info:
        await journal_entry_repo.get_journal_entry("non-existent-id")

    error = exc_info.value

    assert error.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio
async def test_add_journal_entry_success(
    journal_entry_repo: JournalEntryRepo, sample_technologies
):
    """Test successfully adding a new journal entry with technologies."""
    new_entry = JournalEntryCreate(
        content="New test entry",
        project_id="project1",
        date=datetime(2025, 1, 3),
        technologyIds=[],
        is_private=True,
    )
    result = await journal_entry_repo.add_journal_entry(new_entry, [])
    assert result.content == new_entry.content
    assert result.project_id == new_entry.project_id


@pytest.mark.asyncio
async def test_update_journal_entry_not_found(
    journal_entry_repo: JournalEntryRepo, sample_technologies
):
    """Test updating a non-existent journal entry raises correct error."""
    update_data = JournalEntryUpdate(
        content="Updated content", is_private=False, technologyIds=[]
    )

    with pytest.raises(JournalEntryNotFoundError):
        await journal_entry_repo.update_journal_entry(
            "non-existent-id", update_data, sample_technologies
        )


@pytest.mark.asyncio
async def test_update_journal_entry_success(
    journal_entry_repo: JournalEntryRepo, mocker
):
    """Test successful journal entry update with technologies."""
    # Arrange
    test_id = "test-id"
    original_entry = JournalEntry(
        id=test_id, content="Original content", is_private=False, technologies=[]
    )

    update_data = JournalEntryUpdate(
        content="Updated content", is_private=True, technologyIds=["tech-1", "tech-2"]
    )

    new_technologies = [
        Technology(id="tech-1", name="Python"),
        Technology(id="tech-2", name="React"),
    ]

    mock_get = mocker.patch.object(
        journal_entry_repo, "get_journal_entry", return_value=original_entry
    )

    mock_save = mocker.patch.object(
        journal_entry_repo, "_save_journal_entry", return_value=original_entry
    )

    # Act
    result = await journal_entry_repo.update_journal_entry(
        test_id, update_data, new_technologies
    )

    # Assert
    mock_get.assert_called_once_with(test_id)
    mock_save.assert_called_once()
    assert result.content == "Updated content"
    assert result.is_private is True
    assert result.technologies == new_technologies


@pytest.mark.asyncio
async def test_save_journal_entry_database_error(
    journal_entry_repo: JournalEntryRepo, sample_journal_entries, mocker
):
    """Test database error handling when saving a journal entry."""
    mocker.patch.object(
        journal_entry_repo.session,
        "commit",
        side_effect=SQLAlchemyError("Database error"),
    )

    with pytest.raises(SQLAlchemyError):
        await journal_entry_repo._save_journal_entry(sample_journal_entries[0])
