from enums import Language
from sqlmodel import SQLModel


class Technology_Create(SQLModel):
    """Data transfer object for creating a new Technology record"""

    name: str
    description: str | None = None
    language: Language | None = None
