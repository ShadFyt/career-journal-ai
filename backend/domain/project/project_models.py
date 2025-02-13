from sqlmodel import SQLModel


class Project_Create(SQLModel):
    name: str
    description: str | None = None
    link: str | None = None
    is_private: bool = False
