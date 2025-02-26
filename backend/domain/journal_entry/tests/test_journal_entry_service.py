"""Tests for the journal entry service layer."""

from unittest.mock import AsyncMock, Mock

import pytest
from database.models import JournalEntry, Technology
from domain.journal_entry.journal_entry_exceptions import JournalEntryNotFoundError
from domain.journal_entry.journal_entry_schema import (
    JournalEntryCreate,
    JournalEntryRead,
    JournalEntryUpdate,
)
from domain.journal_entry.journal_entry_service import JournalEntryService
from domain.technology.technology_exceptions import TechnologyNotFoundError

mock_user_id = "123"


@pytest.fixture
def mock_repo():
    """Fixture for mocked JournalEntryRepo."""
    return Mock(
        get_journal_entries=AsyncMock(),
        get_journal_entry=AsyncMock(),
        add_journal_entry=AsyncMock(),
        update_journal_entry=AsyncMock(),
    )


@pytest.fixture
def mock_tech_service():
    """Fixture for mocked TechnologyService."""
    return Mock(get_technologies_by_ids=AsyncMock())


@pytest.fixture
def journal_entry_service(mock_repo, mock_tech_service):
    """Fixture for JournalEntryService with mocked dependencies."""
    return JournalEntryService(mock_repo, mock_tech_service)


@pytest.fixture
def sample_technologies():
    """Fixture for sample technology data."""
    return [
        Technology(id="tech-1", name="Python"),
        Technology(id="tech-2", name="React"),
    ]


@pytest.fixture
def sample_journal_entry():
    """Fixture for sample journal entry data."""
    return JournalEntry(
        id="test-id", content="Test content", is_private=False, technologies=[]
    )


@pytest.mark.asyncio
async def test_get_journal_entries(
    journal_entry_service, mock_repo, sample_journal_entry
):
    """Test getting all journal entries."""
    # Arrange
    mock_repo.get_journal_entries.return_value = [sample_journal_entry]

    # Act
    result = await journal_entry_service.get_journal_entries()

    # Assert
    assert result == [sample_journal_entry]
    mock_repo.get_journal_entries.assert_called_once()


@pytest.mark.asyncio
async def test_get_journal_entry(
    journal_entry_service, mock_repo, sample_journal_entry
):
    """Test getting a specific journal entry."""
    # Arrange
    mock_repo.get_journal_entry.return_value = sample_journal_entry

    # Act
    result = await journal_entry_service.get_journal_entry("test-id")

    # Assert
    assert result == sample_journal_entry
    mock_repo.get_journal_entry.assert_called_once_with("test-id")


@pytest.mark.asyncio
async def test_get_journal_entry_not_found(journal_entry_service, mock_repo):
    """Test getting a non-existent journal entry."""
    # Arrange
    mock_repo.get_journal_entry.side_effect = JournalEntryNotFoundError(
        message="Not found"
    )

    # Act & Assert
    with pytest.raises(JournalEntryNotFoundError):
        await journal_entry_service.get_journal_entry("non-existent-id")


@pytest.mark.asyncio
async def test_add_journal_entry_success(
    journal_entry_service,
    mock_repo,
    mock_tech_service,
    sample_technologies,
    sample_journal_entry,
):
    """Test successful journal entry creation."""
    # Arrange
    create_data = JournalEntryCreate(
        content="Test content",
        is_private=False,
        technologyIds=["tech-1", "tech-2"],
        user_id=mock_user_id,
    )

    mock_tech_service.get_technologies_by_ids.return_value = sample_technologies
    mock_repo.add_journal_entry.return_value = sample_journal_entry

    # Act
    result = await journal_entry_service.add_journal_entry(create_data)

    # Assert
    assert isinstance(result, JournalEntryRead)
    mock_tech_service.get_technologies_by_ids.assert_called_once_with(
        create_data.technologyIds
    )
    mock_repo.add_journal_entry.assert_called_once_with(
        create_data, sample_technologies
    )


@pytest.mark.asyncio
async def test_add_journal_entry_tech_not_found(
    journal_entry_service, mock_tech_service
):
    """Test journal entry creation with invalid technology IDs."""
    # Arrange
    create_data = JournalEntryCreate(
        content="Test content",
        is_private=False,
        technologyIds=["invalid-id"],
        user_id=mock_user_id,
    )

    mock_tech_service.get_technologies_by_ids.side_effect = TechnologyNotFoundError(
        message="Tech not found"
    )

    # Act & Assert
    with pytest.raises(TechnologyNotFoundError):
        await journal_entry_service.add_journal_entry(create_data)


@pytest.mark.asyncio
async def test_update_journal_entry_success(
    journal_entry_service,
    mock_repo,
    mock_tech_service,
    sample_technologies,
    sample_journal_entry,
):
    """Test successful journal entry update."""
    # Arrange
    update_data = JournalEntryUpdate(
        content="Updated content", is_private=True, technologyIds=["tech-1", "tech-2"]
    )

    mock_tech_service.get_technologies_by_ids.return_value = sample_technologies
    mock_repo.update_journal_entry.return_value = sample_journal_entry

    # Act
    result = await journal_entry_service.update_journal_entry("test-id", update_data)

    # Assert
    assert isinstance(result, JournalEntryRead)
    mock_tech_service.get_technologies_by_ids.assert_called_once_with(
        update_data.technologyIds
    )
    mock_repo.update_journal_entry.assert_called_once_with(
        "test-id", update_data, sample_technologies
    )


@pytest.mark.asyncio
async def test_update_journal_entry_without_technologies(
    journal_entry_service, mock_repo, sample_journal_entry
):
    """Test journal entry update without technology changes."""
    # Arrange
    update_data = JournalEntryUpdate(
        content="Updated content", is_private=True, technologyIds=None
    )

    mock_repo.update_journal_entry.return_value = sample_journal_entry

    # Act
    result = await journal_entry_service.update_journal_entry("test-id", update_data)

    # Assert
    assert isinstance(result, JournalEntryRead)
    mock_repo.update_journal_entry.assert_called_once_with("test-id", update_data, None)


@pytest.mark.asyncio
async def test_update_journal_entry_tech_not_found(
    journal_entry_service, mock_tech_service
):
    """Test journal entry update with invalid technology IDs."""
    # Arrange
    update_data = JournalEntryUpdate(
        content="Updated content", is_private=True, technologyIds=["invalid-id"]
    )

    mock_tech_service.get_technologies_by_ids.side_effect = TechnologyNotFoundError(
        message="Tech not found"
    )

    # Act & Assert
    with pytest.raises(TechnologyNotFoundError):
        await journal_entry_service.update_journal_entry("test-id", update_data)
