import pytest
from domain.journal_entry.journal_entry_repo import JournalEntryRepo
from domain.journal_entry.journal_entry_service import JournalEntryService

# flake8: noqa: F401
from tests.conftest import *


@pytest.fixture
def journal_entry_repo(db_session) -> JournalEntryRepo:
    """Create a JournalEntryRepo instance for testing."""
    return JournalEntryRepo(db_session)


@pytest.fixture
def journal_entry_service(journal_entry_repo: JournalEntryRepo) -> JournalEntryService:
    """Create a JournalEntryService instance for testing."""
    return JournalEntryService(journal_entry_repo)
