import datetime

from authx import TokenPayload
from domain.auth.auth_config import security
from domain.auth.auth_dependencies import AuthDeps, AuthServiceDep
from domain.auth.auth_schema import AuthSuccess, LoginRequest
from fastapi import APIRouter, Depends, Response, status

router = APIRouter()


@router.get(
    "/session",
    status_code=status.HTTP_200_OK,
    response_model=AuthSuccess,
    dependencies=[*AuthDeps],
)
async def get_session(payload: TokenPayload = Depends(security.access_token_required)):
    return {
        "email": payload.email,
        "user_id": payload.user_id,
        "first_name": payload.first_name,
        "last_name": payload.last_name,
    }


@router.post("/login", status_code=status.HTTP_200_OK, response_model=AuthSuccess)
async def login(
    service: AuthServiceDep,
    login_data: LoginRequest,
    response: Response,
):
    auth_payload = await service.login(login_data.email, login_data.password)

    security.set_access_cookies(auth_payload["access_token"], response)
    if login_data.remember_me:
        security.set_refresh_cookies(
            auth_payload["refresh_token"],
            response,
        )
    return auth_payload


@router.post("/logout", status_code=status.HTTP_200_OK)
async def logout(response: Response):
    security.unset_access_cookies(response)
    security.unset_refresh_cookies(response)

    return {"message": "Successfully logged out"}
