from datetime import datetime
from mailbox import Message
from pydantic import NonNegativeFloat
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, Mock
from domain.journal_entry.journal_entry_router import router
from domain.journal_entry.journal_entry_exceptions import JournalEntryNotFoundError
from domain.technology.technology_exceptions import TechnologyNotFoundError
from domain.journal_entry.journal_entry_dependencies import get_journal_entry_service
from domain.journal_entry.journal_entry_service import JournalEntryService
from domain.journal_entry.journal_entry_schema import (
    JournalEntryCreate,
    JournalEntryUpdate,
)
from database.models import JournalEntry

mock_journal_entry = [
    JournalEntry(
        id="new-id",
        content="new content",
        is_private=False,
        project_id=None,
        technologies=[],
    ),
    JournalEntry(
        id="old-id",
        content="old content",
        is_private=True,
        project_id="project1",
        technologies=[],
    ),
]


@pytest.fixture
def mock_service(mocker):
    """Fixture for mocked JournalEntryService."""
    mock = mocker.Mock(spec=JournalEntryService)
    mock.add_journal_entry = mocker.AsyncMock()
    return mock


@pytest.fixture
def app(mock_service):
    """Fixture for FastAPI test app."""
    app = FastAPI()
    app.include_router(router)

    app.dependency_overrides[get_journal_entry_service] = lambda: mock_service

    return app


@pytest.fixture
def client(app):
    """Fixture for FastAPI test client."""
    return TestClient(app)


class TestGetJournalEntries:
    def test_get_journal_entries_success(self, client, mock_service):
        """Test successful retrieval of all journal entries."""
        # Arrange
        mock_service.get_journal_entries.return_value = mock_journal_entry

        # Act
        response = client.get("/journal-entries/")

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        assert data[0]["id"] == mock_journal_entry[0].id
        assert data[0]["content"] == mock_journal_entry[0].content
        mock_service.get_journal_entries.assert_called_once()

    def test_get_journal_entries_empty(self, client, mock_service):
        """Test retrieval of empty journal entries list."""
        # Arrange
        mock_service.get_journal_entries.return_value = []

        # Act
        response = client.get("/journal-entries/")

        # Assert
        assert response.status_code == 200
        assert response.json() == []


class TestGetJournalEntry:
    def test_get_journal_entry_success(self, client, mock_service):
        """Test successful retrieval of a specific journal entry."""
        # Arrange
        mock_service.get_journal_entry.return_value = mock_journal_entry[0]

        # Act
        response = client.get(f"/journal-entries/{mock_journal_entry[0].id}")

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == mock_journal_entry[0].id
        assert data["content"] == mock_journal_entry[0].content
        mock_service.get_journal_entry.assert_called_once_with(mock_journal_entry[0].id)

    def test_get_journal_entry_not_found(self, client, mock_service):
        """Test retrieval of non-existent journal entry."""
        # Arrange
        mock_service.get_journal_entry.side_effect = JournalEntryNotFoundError(
            message="Not found"
        )

        # Act
        response = client.get("/journal-entries/non-existent-id")

        # Assert
        assert response.status_code == 404


class TestAddJournalEntry:
    def test_add_journal_entry_success(self, client, mock_service):
        """Test successful journal entry creation."""
        # Arrange
        create_data = JournalEntryCreate(
            content="Test content",
            is_private=False,
            technologyIds=[],
        )
        mock_response = JournalEntry(**create_data.model_dump(), id="test-id")
        mock_service.add_journal_entry.return_value = mock_response

        # Act
        response = client.post("/journal-entries/", json=create_data.model_dump())

        # Assert
        assert response.status_code == 201
        data = response.json()
        assert data["id"] == mock_response.id

    def test_add_journal_entry_invalid_data(self, client):
        """Test journal entry creation with invalid data."""
        # Arrange
        invalid_data = {
            "is_private": False,
            "technologyIds": ["tech-1"],
            # Missing required 'content' field
        }

        # Act
        response = client.post("/journal-entries/", json=invalid_data)

        # Assert
        assert response.status_code == 422


class TestUpdateJournalEntry:
    def test_update_journal_entry_success(self, client, mock_service):
        """Test successful journal entry update."""
        # Arrange
        update_data = JournalEntryUpdate(
            content="Updated content", is_private=True, technologyIds=[]
        )
        mock_result = JournalEntry(
            **update_data.model_dump(), id=mock_journal_entry[0].id
        )
        mock_service.update_journal_entry.return_value = mock_result

        # Act
        response = client.patch(
            f"/journal-entries/{mock_journal_entry[0].id}",
            json=update_data.model_dump(),
        )

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["content"] == "Updated content"

    def test_update_journal_entry_not_found(self, client, mock_service):
        """Test update of non-existent journal entry."""
        # Arrange
        update_data = {
            "content": "Updated content",
            "is_private": True,
            "technologyIds": ["tech-1"],
        }
        mock_service.update_journal_entry.side_effect = JournalEntryNotFoundError(
            message="Not found"
        )

        # Act
        response = client.patch("/journal-entries/non-existent-id", json=update_data)

        # Assert
        assert response.status_code == 404


class TestDeleteJournalEntry:
    def test_delete_journal_entry_not_implemented(self, client):
        """Test journal entry deletion (not implemented)."""
        # Act
        response = client.delete("/journal-entries/test-id")

        # Assert
        assert response.status_code == 501
        assert "not yet implemented" in response.json()["detail"]["message"]
