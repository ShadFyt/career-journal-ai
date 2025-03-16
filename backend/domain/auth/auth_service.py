from datetime import timedelta
from typing import TypedDict

from database.models import User
from domain.auth.auth_config import security
from domain.auth.auth_schema import AuthSuccess
from domain.user.user_service import UserService
from fastapi import HTTPException


class Tokens(TypedDict):
    access_token: str
    refresh_token: str


class AuthService:
    def __init__(self, user_service: UserService) -> None:
        self.user_service = user_service

    async def login(self, email: str, password: str) -> AuthSuccess:
        user = await self.user_service.get_user_by_email(email)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        if not self.user_service.check_password(password, user.password):
            raise HTTPException(status_code=401, detail="Invalid credentials")

        tokens = await self.create_tokens(user)

        return {
            "email": user.email,
            "user_id": user.id,
            **tokens,
        }

    async def create_tokens(self, user: User) -> Tokens:
        token = security.create_access_token(
            user.id,
            data={"email": user.email, "user_id": user.id},
            expiry=timedelta(days=1),
        )
        refresh_token = security.create_refresh_token(
            user.id,
            data={"email": user.email, "user_id": user.id},
            expiry=timedelta(days=14),
        )

        return {
            "access_token": token,
            "refresh_token": refresh_token,
        }
