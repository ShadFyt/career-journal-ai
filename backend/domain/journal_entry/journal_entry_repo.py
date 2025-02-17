from database.models import JournalEntry, Technology
from database.session import SessionDep
from domain.journal_entry.journal_entry_exceptions import (
    JournalEntryDatabaseError,
    JournalEntryNotFoundError,
)
from domain.journal_entry.journal_entry_schema import JournalEntryCreate
from sqlalchemy.exc import SQLAlchemyError
from sqlmodel import select


class JournalEntryRepo:
    def __init__(self, session: SessionDep):
        self.session = session

    def get_journal_entries(self) -> list[JournalEntry]:
        """Get all journal entries sorted by date and name.

        Returns:
            list[JournalEntry]: List of all journal entries

        Raises:
            JournalEntryDatabaseError: If database operation fails
        """

        try:
            statement = select(JournalEntry).order_by(JournalEntry.date.desc())
            return self.session.exec(statement).all()

        except SQLAlchemyError as e:
            raise JournalEntryDatabaseError(
                message=f"Failed to fetch journal entries: {str(e)}"
            )

    def get_journal_entry(self, id: str) -> JournalEntry:
        """Get a single journal entry by ID.

        Args:
            id (str): Journal entry ID

        Returns:
            JournalEntry: The requested journal entry

        Raises:
            JournalEntryNotFoundError: If journal entry not found or database operation fails
        """
        try:
            found_entry = self.session.get(JournalEntry, id)
            if not found_entry:
                raise JournalEntryNotFoundError(
                    message=f"Journal entry with ID '{id}' not found",
                )
            return found_entry

        except SQLAlchemyError as e:
            raise JournalEntryDatabaseError(
                message=f"Failed to fetch journal entry: {str(e)}"
            )

    def add_journal_entry(
        self, journal_entry_create: JournalEntryCreate, technologies: list[Technology]
    ):
        new_journal_entry = JournalEntry(
            **journal_entry_create.model_dump(), technologies=technologies
        )
        return self._save_journal_entry(new_journal_entry)

    def update_journal_entry(self, id: str):
        pass

    def _save_journal_entry(self, journal_entry: JournalEntry) -> JournalEntry:
        """Save journal entry to database and refresh.

        Args:
            journal_entry: JournalEntry instance to save

        Returns:
            JournalEntry: Refreshed journal entry instance

        Raises:
            SQLAlchemyError: If database operation fails
        """
        self.session.add(journal_entry)
        self.session.commit()
        self.session.refresh(journal_entry)
        return journal_entry
