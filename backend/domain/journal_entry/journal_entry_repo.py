from database.models import JournalEntry, Technology
from database.session import SessionDep
from domain.journal_entry.journal_entry_exceptions import (
    JournalEntryDatabaseError,
    JournalEntryNotFoundError,
)
from domain.journal_entry.journal_entry_schema import (
    JournalEntryCreate,
    JournalEntryUpdate,
)
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import selectinload
from sqlmodel import select


class JournalEntryRepo:
    def __init__(self, session: SessionDep):
        self.session = session

    async def get_journal_entries(self) -> list[JournalEntry]:
        """Get all journal entries sorted by date and name.

        Returns:
            list[JournalEntry]: List of all journal entries

        Raises:
            JournalEntryDatabaseError: If database operation fails
        """

        try:
            statement = (
                select(JournalEntry)
                .options(selectinload(JournalEntry.technologies))
                .order_by(JournalEntry.date.desc())
            )
            results = await self.session.exec(statement)
            return results.all()

        except SQLAlchemyError as e:
            raise JournalEntryDatabaseError(
                message=f"Failed to fetch journal entries: {str(e)}"
            )

    async def get_journal_entry(self, id: str) -> JournalEntry:
        """Get a single journal entry by ID.

        Args:
            id (str): Journal entry ID

        Returns:
            JournalEntry: The requested journal entry

        Raises:
            JournalEntryNotFoundError: If journal entry not found or database operation fails
        """
        try:
            found_entry = await self.session.get(JournalEntry, id)
            if not found_entry:
                raise JournalEntryNotFoundError(
                    message=f"Journal entry with ID '{id}' not found",
                )
            return found_entry

        except SQLAlchemyError as e:
            raise JournalEntryDatabaseError(
                message=f"Failed to fetch journal entry: {str(e)}"
            )

    async def add_journal_entry(
        self, journal_entry_create: JournalEntryCreate, technologies: list[Technology]
    ):
        new_journal_entry = JournalEntry(
            **journal_entry_create.model_dump(), technologies=technologies
        )
        return await self._save_journal_entry(new_journal_entry)

    async def update_journal_entry(
        self, id: str, entry: JournalEntryUpdate, technologies: list[Technology] | None
    ):
        """Update an existing journal entry.

        Args:
            id: The ID of the journal entry to update.
            entry: The update data.
            technologies: The updated technologies associated with the journal entry.

        Returns:
            The updated journal entry.

        Raises:
            JournalEntryNotFoundError: If the journal entry does not exist.
        """
        db_journal_entry = await self.get_journal_entry(id)
        journal_entry_data = entry.model_dump(exclude_unset=True)
        for key, value in journal_entry_data.items():
            if key != "technologyIds":
                setattr(db_journal_entry, key, value)
        if technologies is not None:
            db_journal_entry.technologies = technologies
        return await self._save_journal_entry(db_journal_entry)

    async def _save_journal_entry(self, journal_entry: JournalEntry) -> JournalEntry:
        """Save journal entry to database and refresh.

        Args:
            journal_entry: JournalEntry instance to save

        Returns:
            JournalEntry: Refreshed journal entry instance

        Raises:
            SQLAlchemyError: If database operation fails
            SQLAlchemyError: If database operation fails
        """
        self.session.add(journal_entry)
        await self.session.commit()
        await self.session.refresh(journal_entry)
        return journal_entry
