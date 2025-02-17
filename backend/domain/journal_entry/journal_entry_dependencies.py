from typing import Annotated

from database.session import SessionDep
from domain.journal_entry.journal_entry_repo import JournalEntryRepo
from domain.journal_entry.journal_entry_service import JournalEntryService
from fastapi import Depends
from domain.technology.technology_dependencies import get_technology_service
from domain.technology.technology_service import TechnologyService


def get_journal_entry_repo(session: SessionDep) -> JournalEntryRepo:
    return JournalEntryRepo(session=session)


def get_journal_entry_service(
    repo: JournalEntryRepo = Depends(get_journal_entry_repo),
    technology_service: TechnologyService = Depends(get_technology_service),
) -> JournalEntryService:
    return JournalEntryService(repo=repo, technology_service=technology_service)


JournalEntryServiceDep = Annotated[
    JournalEntryService, Depends(get_journal_entry_service)
]
