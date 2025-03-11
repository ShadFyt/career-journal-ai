from core.schema.base import BaseSchema


class AuthSuccess(BaseSchema):
    access_token: str
    refresh_token: str | None
    email: str
    user_id: str


class LoginRequest(BaseSchema):
    email: str
    password: str
