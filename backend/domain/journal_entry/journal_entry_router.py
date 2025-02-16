from domain.journal_entry.dependencies import JournalEntryServiceDep
from fastapi import APIRouter, status

router = APIRouter(prefix="/journal-entries", tags=["journal-entries"])


@router.get("/")
async def get_journal_entries(
    service: JournalEntryServiceDep,
):
    pass


@router.post("/", status_code=status.HTTP_201_CREATED)
async def add_journal_entry(
    service: JournalEntryServiceDep,
):
    pass


@router.get("/{id}")
async def get_journal_entry(
    id: str,
    service: JournalEntryServiceDep,
):
    pass


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
