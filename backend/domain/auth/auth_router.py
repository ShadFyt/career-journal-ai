from domain.auth.auth_config import security
from domain.auth.auth_dependencies import AuthServiceDep
from domain.auth.auth_schema import AuthSuccess, LoginRequest
from fastapi import APIRouter, Response, status

router = APIRouter()

ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 1 day
REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 7 days


@router.post("/login", status_code=status.HTTP_200_OK, response_model=AuthSuccess)
async def login(
    service: AuthServiceDep,
    login_data: LoginRequest,
    response: Response,
):
    auth_payload = await service.login(login_data.email, login_data.password)

    security.set_access_cookies(
        auth_payload["access_token"], response, max_age=ACCESS_TOKEN_EXPIRE_MINUTES
    )
    if login_data.remember_me:
        security.set_refresh_cookies(
            auth_payload["refresh_token"],
            response,
            max_age=REFRESH_TOKEN_EXPIRE_MINUTES,
        )
    return {"message": "Successfully logged in"}


@router.post("/logout")
async def logout():
    security.unset_access_cookies()
    security.unset_refresh_cookies()
    return {"message": "Successfully logged out"}
