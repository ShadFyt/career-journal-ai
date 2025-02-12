from fastapi import APIRouter
from sqlmodel import select

from database.session import SessionDep
from database.models import Technology

router = APIRouter()


@router.get("/")
async def get_technologies(session: SessionDep) -> list[Technology]:
    return session.exec(select(Technology)).all()
