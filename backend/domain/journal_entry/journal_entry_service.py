from domain.journal_entry.journal_entry_repo import JournalEntryRepo
from domain.journal_entry.journal_entry_schema import (
    JournalEntryCreate,
    JournalEntryRead,
)
from domain.technology.technology_service import TechnologyService


class JournalEntryService:
    def __init__(
        self, repo: JournalEntryRepo, technology_service: TechnologyService
    ) -> None:
        self.repo = repo
        self.technology_service = technology_service

    async def get_journal_entries(self):
        return await self.repo.get_journal_entries()

    async def get_journal_entry(self, id: str):
        return await self.repo.get_journal_entry(id)

    async def add_journal_entry(self, journal_entry_create: JournalEntryCreate):
        technologies = await self.technology_service.get_technologies_by_ids(
            journal_entry_create.technologyIds
        )
        journal_entry = await self.repo.add_journal_entry(
            journal_entry_create, technologies
        )
        return JournalEntryRead(**journal_entry.dict(), technologies=technologies)

    async def update_journal_entry(self, id: str):
        pass
