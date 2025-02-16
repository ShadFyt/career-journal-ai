from datetime import datetime
from typing import Any

from pydantic import BaseModel


class Project_Base(BaseModel):
    """Base model for project data transfer."""

    name: str
    description: str | None = None
    link: str | None = None
    is_private: bool = False


class Project_Create(Project_Base):
    """Input model for creating a new project."""

    pass


class Project_Read(Project_Base):
    """Output model for project responses."""

    id: str
    last_entry_date: datetime | None = None
