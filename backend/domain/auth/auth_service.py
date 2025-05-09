from datetime import datetime, timedelta, timezone
from typing import TypedDict, Any, Coroutine

from authx import TokenPayload
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

    async def login(self, email: str, password: str) -> dict[str, str]:
        user = await self.user_service.get_user_by_email(email)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        if not self.user_service.check_password(password, user.password):
            raise HTTPException(status_code=401, detail="Invalid credentials")

        tokens = await self.create_tokens(user)

        return {
            "email": user.email,
            "user_id": user.id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            **tokens,
        }

    async def refresh_access_token(self, payload: TokenPayload):
        today = datetime.now(timezone.utc)
        if payload.exp < today:
            raise HTTPException(status_code=401, detail="Refresh token expired")

        user = await self.user_service.get_user(payload.user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        tokens = await self.create_tokens(user)
        return tokens["access_token"]

    async def create_tokens(self, user: User) -> Tokens:
        token_payload = {
            "email": user.email,
            "user_id": user.id,
            "first_name": user.first_name,
            "last_name": user.last_name,
        }
        token = security.create_access_token(
            user.id,
            data=token_payload,
            expiry=timedelta(days=1),
        )
        refresh_token = security.create_refresh_token(
            user.id,
            data=token_payload,
            expiry=timedelta(days=14),
        )

        return {
            "access_token": token,
            "refresh_token": refresh_token,
        }
