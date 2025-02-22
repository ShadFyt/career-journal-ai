from datetime import datetime
from typing import Optional

from database.models import Technology
from pydantic import BaseModel


class JournalEntryBase(BaseModel):
    content: str
    is_private: bool
    project_id: str | None = None


class JournalEntryRead(JournalEntryBase):
    id: str
    date: datetime
    technologies: list[Technology]


class JournalEntryCreate(JournalEntryBase):
    technologyIds: list[str]


class JournalEntryUpdate(BaseModel):
    content: Optional[str] = None
    is_private: Optional[bool] = None
    project_id: Optional[str] = None
    technologyIds: Optional[list[str]] = None
