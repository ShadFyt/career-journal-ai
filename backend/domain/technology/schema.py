from enums import Language
from pydantic import BaseModel


class TechnologyBase(BaseModel):
    name: str
    description: str | None = None
    language: Language | None = None


class TechnologyRead(TechnologyBase):
    id: str


class Technology_Create(TechnologyBase):
    """Data transfer object for creating a new Technology record"""


class TechnologyWithCount(TechnologyRead):
    """Technology data with usage count"""

    usage_count: int
