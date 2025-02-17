from domain.journal_entry.journal_entry_repo import JournalEntryRepo
from domain.technology.technology_service import TechnologyService
from domain.journal_entry.journal_entry_schema import JournalEntryCreate


class JournalEntryService:
    def __init__(self, repo: JournalEntryRepo, technology_service: TechnologyService) -> None:
        self.repo = repo
        self.technology_service = technology_service

    def get_journal_entries(self):
        return self.repo.get_journal_entries()

    def get_journal_entry(self, id: str):
        return self.repo.get_journal_entry(id)

    def add_journal_entry(self, journal_entry_create: JournalEntryCreate):
        technologies = self.technology_service.get_technologies_by_ids(journal_entry_create.technologyIds)
        return self.repo.add_journal_entry(journal_entry_create, technologies)

    def update_journal_entry(self, id: str):
        pass
