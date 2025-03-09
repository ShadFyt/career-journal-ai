from domain.auth.auth_dependencies import AuthServiceDep
from domain.auth.auth_schema import AuthSuccess
from fastapi import APIRouter, status

router = APIRouter()


@router.post("/login", status_code=status.HTTP_200_OK, response_model=AuthSuccess)
async def login(
    service: AuthServiceDep,
    email: str,
    password: str,
):
    return await service.login(email, password)


@router.post("/logout")
async def logout():
    pass
