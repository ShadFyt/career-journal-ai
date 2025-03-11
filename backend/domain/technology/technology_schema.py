from core.schema.base import BaseSchema
from enums import Language


class TechnologyBase(BaseSchema):
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
