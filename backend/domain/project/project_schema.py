from datetime import datetime

from pydantic import BaseModel


class ProjectBase(BaseModel):
    """Base model for project data transfer."""

    name: str
    description: str | None = None
    link: str | None = None
    is_private: bool = False


class ProjectCreate(ProjectBase):
    """Input model for creating a new project."""

    user_id: str


class ProjectRead(ProjectBase):
    """Output model for project responses."""

    id: str
    last_entry_date: datetime | None = None


class ProjectUpdate(ProjectBase):
    """Input model for updating an existing project."""

    pass
