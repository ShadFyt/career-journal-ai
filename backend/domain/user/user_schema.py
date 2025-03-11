from core.schema.base import BaseSchema


class UserBase(BaseSchema):
    email: str
    first_name: str
    last_name: str


class UserCreate(UserBase):
    password: str


class UserUpdate(UserBase):
    password: str | None = None


class UserRead(UserBase):
    id: str
