from datetime import datetime
from sqlmodel import Field, SQLModel
from uuid import uuid4
from enums import Language


class JournalEntry(SQLModel, table=True):
    id: str = Field(primary_key=True, default_factory=uuid4, nullable=False)
    content: str
    date: datetime = Field(default_factory=datetime.now)


class Technology(SQLModel, table=True):
    id: str = Field(primary_key=True, default_factory=uuid4, nullable=False)
    name: str = Field(index=True)
    description: str | None = Field(default=None)
    language: Language = Field(default=Language.TYPESCRIPT)
