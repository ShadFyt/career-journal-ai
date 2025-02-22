from domain.journal_entry.journal_entry_dependencies import JournalEntryServiceDep
from domain.journal_entry.journal_entry_schema import (
    JournalEntryCreate,
    JournalEntryRead,
    JournalEntryUpdate,
)
from fastapi import APIRouter, HTTPException, status

router = APIRouter(prefix="/journal-entries", tags=["journal-entries"])


@router.get("/", response_model=list[JournalEntryRead])
async def get_journal_entries(
    service: JournalEntryServiceDep,
):
    """Get all journal entries.

    Returns:
        list[JournalEntryRead]: List of journal entries sorted by date (descending)
    """
    return await service.get_journal_entries()


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=JournalEntryRead)
async def add_journal_entry(
    service: JournalEntryServiceDep,
    journal_entry_create: JournalEntryCreate,
):
    """Create a new journal entry.

    Args:
        journal_entry_create (JournalEntryCreate): Journal entry data

    Returns:
        JournalEntryRead: The created journal entry with associated technologies
    """
    return await service.add_journal_entry(journal_entry_create)


@router.get("/{id}")
async def get_journal_entry(
    id: str,
    service: JournalEntryServiceDep,
):
    """Get a specific journal entry by ID.

    Args:
        id (str): Journal entry ID

    Returns:
        JournalEntry: The requested journal entry

    Raises:
        HTTPException: 404 if journal entry not found
    """
    return await service.get_journal_entry(id)


@router.patch("/{id}")
async def update_journal_entry(
    id: str,
    service: JournalEntryServiceDep,
    journal_entry_update: JournalEntryUpdate,
):
    """Update a journal entry.

    Args:
        id (str): Journal entry ID

    Returns:
        JournalEntry: The updated journal entry

    Raises:
        HTTPException: 404 if journal entry not found
    """
    return await service.update_journal_entry(id, journal_entry_update)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_journal_entry(
    id: str,
    service: JournalEntryServiceDep,
):
    """Delete a journal entry.

    Args:
        id (str): Journal entry ID

    Raises:
        HTTPException: 404 if journal entry not found
    """
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail={"message": "Journal entry deletion is not yet implemented"},
    )
