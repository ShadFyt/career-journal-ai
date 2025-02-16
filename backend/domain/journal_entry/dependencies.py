from database.session import SessionDep
from domain.journal_entry.journal_entry_repo import JournalEntryRepo
from domain.journal_entry.journal_entry_service import JournalEntryService
from fastapi import Depends


def get_journal_entry_repo(session: SessionDep) -> JournalEntryRepo:
    return JournalEntryRepo(session=session)


def get_journal_entry_service(
    repo: JournalEntryRepo = Depends(get_journal_entry_repo),
) -> JournalEntryService:
    return JournalEntryService(repo=repo)
