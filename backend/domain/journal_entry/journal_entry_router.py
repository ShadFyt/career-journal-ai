from domain.journal_entry.dependencies import get_journal_entry_service
from domain.journal_entry.journal_entry_service import JournalEntryService
from fastapi import APIRouter, Depends, status

router = APIRouter(prefix="/journal-entries", tags=["journal-entries"])


@router.get("/")
async def get_journal_entries(
    service: JournalEntryService = Depends(get_journal_entry_service),
):
    pass


@router.post("/", status_code=status.HTTP_201_CREATED)
async def add_journal_entry(
    service: JournalEntryService = Depends(get_journal_entry_service),
):
    pass


@router.get("/{id}")
async def get_journal_entry(
    id: str,
    service: JournalEntryService = Depends(get_journal_entry_service),
):
    pass


@router.patch("/{id}")
async def update_journal_entry(
    id: str,
    service: JournalEntryService = Depends(get_journal_entry_service),
):
    pass


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_journal_entry(
    id: str,
    service: JournalEntryService = Depends(get_journal_entry_service),
):
    pass
