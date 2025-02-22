from domain.journal_entry.journal_entry_repo import JournalEntryRepo
from domain.journal_entry.journal_entry_schema import (
    JournalEntryCreate,
    JournalEntryRead,
    JournalEntryUpdate,
)
from domain.technology.technology_service import TechnologyService


class JournalEntryService:
    def __init__(
        self, repo: JournalEntryRepo, technology_service: TechnologyService
    ) -> None:
        """Initialize JournalEntryService with dependencies.

        Args:
            repo: Journal entry repository instance
            technology_service: Technology service instance
        """
        self.repo = repo
        self.technology_service = technology_service

    async def get_journal_entries(self):
        """Get all journal entries.

        Returns:
            list[JournalEntry]: List of all journal entries sorted by date (descending)
        """
        return await self.repo.get_journal_entries()

    async def get_journal_entry(self, id: str):
        """Get a specific journal entry by ID.

        Args:
            id: Journal entry ID

        Returns:
            JournalEntry: The requested journal entry

        Raises:
            JournalEntryNotFoundError: If journal entry not found
        """
        return await self.repo.get_journal_entry(id)

    async def add_journal_entry(self, journal_entry_create: JournalEntryCreate):
        """Create a new journal entry.

        Args:
            journal_entry_create: Journal entry creation data
            technologies: List of technologies associated with the journal entry

        Returns:
            JournalEntryRead: The created journal entry with associated technologies

        Raises:
            TechnologyNotFoundError: If any technology ID is invalid
            JournalEntryDatabaseError: If database operation fails
        """
        technologies = await self.technology_service.get_technologies_by_ids(
            journal_entry_create.technologyIds
        )
        journal_entry = await self.repo.add_journal_entry(
            journal_entry_create, technologies
        )
        return JournalEntryRead(**journal_entry.model_dump(), technologies=technologies)

    async def update_journal_entry(self, id: str, entry: JournalEntryUpdate):
        """Update an existing journal entry.

        Args:
            id: Journal entry ID
            entry: Journal entry update data

        Returns:
            JournalEntryRead: The updated journal entry

        Raises:
            JournalEntryNotFoundError: If journal entry not found
            TechnologyNotFoundError: If any technology ID is invalid
            JournalEntryDatabaseError: If database operation fails
        """
        technologies = None
        if entry.technologyIds is not None:
            technologies = await self.technology_service.get_technologies_by_ids(
                entry.technologyIds
            )
        updated_journal_entry = await self.repo.update_journal_entry(
            id, entry, technologies
        )
        return JournalEntryRead(
            **updated_journal_entry.model_dump(),
            technologies=technologies if technologies is not None else [],
        )
