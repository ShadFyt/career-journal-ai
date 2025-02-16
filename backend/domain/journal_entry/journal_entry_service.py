from domain.journal_entry.journal_entry_repo import JournalEntryRepo


class JournalEntryService:
    def __init__(self, repo: JournalEntryRepo) -> None:
        self.repo = repo

    def get_journal_entries(self):
        pass

    def get_journal_entry(self, id: str):
        pass

    def add_journal_entry(self):
        pass

    def update_journal_entry(self, id: str):
        pass

    def delete_journal_entry(self, id: str):
        pass
