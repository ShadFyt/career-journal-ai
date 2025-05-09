from typing import Annotated

from domain.auth.auth_config import security
from domain.auth.auth_service import AuthService
from domain.user.user_dependencies import get_user_service
from domain.user.user_service import UserService
from fastapi import Depends
from fastapi.security import HTTPBearer

http_bearer = HTTPBearer()


def get_auth_service(
    user_service: UserService = Depends(get_user_service),
) -> AuthService:
    return AuthService(user_service=user_service)


AuthServiceDep = Annotated[AuthService, Depends(get_auth_service)]
AuthDeps = [Depends(security.access_token_required)]
