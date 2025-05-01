from core.schema.base import BaseSchema
from enums import Language
from typing import Optional


class TechnologyBase(BaseSchema):
    name: str
    description: str | None = None
    language: Language | None = None


class TechnologyRead(TechnologyBase):
    id: str


class TechnologyCreate(TechnologyBase):
    """Data transfer object for creating a new Technology record"""


class TechnologyWithCount(TechnologyRead):
    """Technology data with usage count"""

    usage_count: int


class TechnologyUpdate(BaseSchema):
    """Data transfer object for partial updates to a Technology record"""

    name: Optional[str] = None
    description: Optional[str] = None
    language: Optional[Language] = None
