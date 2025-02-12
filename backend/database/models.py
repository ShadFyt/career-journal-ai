from datetime import datetime
from sqlmodel import Field, SQLModel, Relationship
from uuid import uuid4
from enums import Language
from typing import List


class JournalEntryTechnologyLink(SQLModel, table=True):
    __tablename__ = "journal_entry_technology_link"
    journal_entry_id: str = Field(foreign_key="journal_entry.id", primary_key=True)
    technology_id: str = Field(foreign_key="technology.id", primary_key=True)


class Technology(SQLModel, table=True):
    __tablename__ = "technology"
    id: str = Field(
        default_factory=lambda: str(uuid4()), primary_key=True, nullable=False
    )
    name: str = Field(index=True)
    description: str | None = Field(default=None)
    language: Language | None = Field(default=None, index=True)
    journal_entries: List["JournalEntry"] = Relationship(
        back_populates="technologies", link_model=JournalEntryTechnologyLink
    )


class JournalEntry(SQLModel, table=True):
    __tablename__ = "journal_entry"
    id: str = Field(
        default_factory=lambda: str(uuid4()), primary_key=True, nullable=False
    )
    content: str
    date: datetime = Field(default_factory=datetime.now)
    is_private: bool = Field(default=False)
    technologies: List["Technology"] = Relationship(
        back_populates="journal_entries", link_model=JournalEntryTechnologyLink
    )
    project_id: str = Field(foreign_key="project.id", index=True)


class Project(SQLModel, table=True):
    __tablename__ = "project"
    id: str = Field(
        default_factory=lambda: str(uuid4()), primary_key=True, nullable=False
    )
    name: str = Field(index=True)
    description: str | None = Field(default=None)
    link: str | None = Field(default=None)
    is_private: bool = Field(default=True)
    last_entry_date: datetime | None = Field(default=None)
    journal_entries: List[JournalEntry] = Relationship()
