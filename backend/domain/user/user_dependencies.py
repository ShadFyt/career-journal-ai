from typing import Annotated

from database.session import SessionDep
from domain.user.user_repo import UserRepo
from domain.user.user_service import UserService
from fastapi import Depends


def get_user_repo(session: SessionDep) -> UserRepo:
    return UserRepo(session=session)


def get_user_service(user_repo: UserRepo = Depends(get_user_repo)) -> UserService:
    return UserService(user_repo=user_repo)


UserServiceDep = Annotated[UserService, Depends(get_user_service)]
