from database.session import SessionDep


class JournalEntryRepo:
    def __init__(self, session: SessionDep):
        self.session = session

    def get_journal_entries(self):
        pass

    def get_journal_entry(self, id: str):
        pass

    def add_journal_entry(self):
        pass

    def update_journal_entry(self, id: str):
        pass

    def delete_journal_entry(self, id: str) -> None:
        pass
