from domain.journal_entry.journal_entry_dependencies import JournalEntryServiceDep
from domain.journal_entry.journal_entry_schema import JournalEntryCreate
from fastapi import APIRouter, status

router = APIRouter(prefix="/journal-entries", tags=["journal-entries"])


@router.get("/")
async def get_journal_entries(
    service: JournalEntryServiceDep,
):
    return service.get_journal_entries()


@router.post("/", status_code=status.HTTP_201_CREATED)
async def add_journal_entry(
    service: JournalEntryServiceDep,
    journal_entry_create: JournalEntryCreate,
):
    return service.add_journal_entry(journal_entry_create)


@router.get("/{id}")
async def get_journal_entry(
    id: str,
    service: JournalEntryServiceDep,
):
    return service.get_journal_entry(id)


@router.patch("/{id}")
async def update_journal_entry(
    id: str,
    service: JournalEntryServiceDep,
):
    pass


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_journal_entry(
    id: str,
    service: JournalEntryServiceDep,
):
    pass
