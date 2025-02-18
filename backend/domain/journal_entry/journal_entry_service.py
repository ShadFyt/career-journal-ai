from domain.journal_entry.journal_entry_repo import JournalEntryRepo
from domain.technology.technology_service import TechnologyService
from domain.journal_entry.journal_entry_schema import JournalEntryCreate


class JournalEntryService:
    def __init__(self, repo: JournalEntryRepo, technology_service: TechnologyService) -> None:
        self.repo = repo
        self.technology_service = technology_service

    async def get_journal_entries(self):
        return await self.repo.get_journal_entries()

    async def get_journal_entry(self, id: str):
        return await self.repo.get_journal_entry(id)

    async def add_journal_entry(self, journal_entry_create: JournalEntryCreate):
        technologies = await self.technology_service.get_technologies_by_ids(journal_entry_create.technologyIds)
        return await self.repo.add_journal_entry(journal_entry_create, technologies)

    async def update_journal_entry(self, id: str):
        pass
