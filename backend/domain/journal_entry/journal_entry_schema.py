from datetime import datetime

from domain.technology.schema import TechnologyRead
from pydantic import BaseModel


class JournalEntryBase(BaseModel):
    content: str
    date: datetime
    is_private: bool
    project_id: str | None


class JournalEntryRead(JournalEntryBase):
    id: str
    technologies: list[TechnologyRead]


class JournalEntryCreate(JournalEntryBase):
    technologies: list[str]
