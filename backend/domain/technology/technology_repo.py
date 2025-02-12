from database.models import Technology
from database.session import SessionDep
from domain.technology.exceptions import TechnologyDatabaseError
from sqlalchemy.exc import SQLAlchemyError
from sqlmodel import select


class TechnologyRepo:
    def __init__(self, session: SessionDep):
        self.session = session

    def get_technologies(self) -> list[Technology]:
        """Get all technologies from the database.

        Returns:
            list[Technology]: List of all technologies

        Raises:
            TechnologyDatabaseError: If database operation fails
        """
        try:
            return self.session.exec(select(Technology)).all()
        except SQLAlchemyError as e:
            raise TechnologyDatabaseError(f"Failed to fetch technologies: {str(e)}")
