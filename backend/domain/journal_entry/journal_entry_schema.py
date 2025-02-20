from datetime import datetime

from database.models import Technology
from pydantic import BaseModel


class JournalEntryBase(BaseModel):
    content: str
    date: datetime
    is_private: bool
    project_id: str | None = None


class JournalEntryRead(JournalEntryBase):
    id: str
    technologies: list[Technology]


class JournalEntryCreate(JournalEntryBase):
    technologyIds: list[str]
