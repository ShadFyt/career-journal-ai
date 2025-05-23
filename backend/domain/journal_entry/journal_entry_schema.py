from datetime import datetime
from typing import Optional

from core.schema.base import BaseSchema
from database.models import Project, Technology


class JournalEntryBase(BaseSchema):
    content: str
    is_private: bool
    project_id: str | None = None


class JournalEntryRead(JournalEntryBase):
    id: str
    date: datetime
    technologies: list[Technology]
    project: Project | None = None


class JournalEntryCreate(JournalEntryBase):
    technologyIds: list[str]


class JournalEntryUpdate(BaseSchema):
    content: Optional[str] = None
    is_private: Optional[bool] = None
    project_id: Optional[str] = None
    technologyIds: Optional[list[str]] = None
