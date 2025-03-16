from core.schema.base import BaseSchema


class AuthSuccess(BaseSchema):
    email: str
    user_id: str


class LoginRequest(BaseSchema):
    email: str
    password: str
    remember_me: bool = False
