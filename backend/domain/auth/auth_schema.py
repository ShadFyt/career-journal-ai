from pydantic import BaseModel


class AuthSuccess(BaseModel):
    access_token: str
    refresh_token: str | None
    email: str
    user_id: str
