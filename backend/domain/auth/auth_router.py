from domain.auth.auth_dependencies import AuthServiceDep
from domain.auth.auth_schema import AuthSuccess, LoginRequest
from fastapi import APIRouter, status

router = APIRouter()


@router.post("/login", status_code=status.HTTP_200_OK, response_model=AuthSuccess)
async def login(
    service: AuthServiceDep,
    login_data: LoginRequest,
):
    return await service.login(login_data.email, login_data.password)


@router.post("/logout")
async def logout():
    pass
