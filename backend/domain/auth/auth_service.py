from domain.auth.auth_config import security
from domain.user.user_service import UserService
from fastapi import HTTPException


class AuthService:
    def __init__(self, user_service: UserService) -> None:
        self.user_service = user_service

    async def login(self, email: str, password: str) -> str:
        print("Login attempt for email:", email)
        user = await self.user_service.get_user_by_email(email)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        if not self.user_service.check_password(password, user.password):
            raise HTTPException(status_code=401, detail="Invalid credentials")

        token = security.create_access_token(user.id, data={"email": email})
        return {
            "access_token": token,
            "email": email,
            "user_id": user.id,
            "refresh_token": None,
        }
