from database.models import Technology
from database.session import SessionDep
from sqlmodel import select


class TechnologyRepo:
    def __init__(self, session: SessionDep):
        self.session = session

    def get_technologies(self) -> list[Technology]:
        return self.session.exec(select(Technology)).all()
