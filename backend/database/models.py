from datetime import datetime
from sqlmodel import Field, SQLModel, Relationship
from uuid import uuid4
from enums import Language


class Technology(SQLModel, table=True):
    id: str = Field(primary_key=True, default_factory=uuid4, nullable=False)
    name: str = Field(index=True)
    description: str | None = Field(default=None)
    language: Language = Field(default=Language.TYPESCRIPT)


class JournalEntry(SQLModel, table=True):
    id: str = Field(primary_key=True, default_factory=uuid4, nullable=False)
    content: str
    date: datetime = Field(default_factory=datetime.now)
    is_private: bool = Field(default=False)
    technologies: list[Technology] = Relationship()
    project_id: str = Field(foreign_key="project.id", index=True)


class Project(SQLModel, table=True):
    id: str = Field(primary_key=True, default_factory=uuid4, nullable=False)
    name: str = Field(index=True)
    description: str | None = Field(default=None)
    link: str | None = Field(default=None)
    is_private: bool = Field(default=True)
    last_entry_date: datetime | None = Field(default=None)
    journal_entries: list[JournalEntry] = Relationship()


class JournalEntryTechnologyLink(SQLModel, table=True):
    journal_entry_id: str = Field(foreign_key="journal_entry.id")
    technology_id: str = Field(foreign_key="technology.id")
