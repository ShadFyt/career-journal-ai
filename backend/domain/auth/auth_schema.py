from core.schema.base import BaseSchema


class AuthSuccess(BaseSchema):
    email: str
    user_id: str
    first_name: str
    last_name: str


class LoginRequest(BaseSchema):
    email: str
    password: str
    remember_me: bool = False
