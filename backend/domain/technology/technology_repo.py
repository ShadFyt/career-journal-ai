from database.models import Technology
from database.session import SessionDep
from domain.technology.exceptions import TechnologyDatabaseError
from domain.technology.technology_models import Technology_Create
from fastapi import status
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
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

    def add_technology(self, technology: Technology_Create) -> Technology:
        """Add a new technology to the database.

        Returns:
            Technology: The newly created technology

        Raises:
            TechnologyDatabaseError: If database operation fails or technology name already exists
        """
        try:
            db_technology = Technology(**technology.model_dump())
            self.session.add(db_technology)
            self.session.commit()
            self.session.refresh(db_technology)
            return db_technology
        except IntegrityError as e:
            self.session.rollback()
            if "UNIQUE constraint failed" in str(e.orig):
                raise TechnologyDatabaseError(
                    f"Technology with name '{technology.name}' already exists",
                    status_code=status.HTTP_400_BAD_REQUEST,
                )
            raise TechnologyDatabaseError(f"Database integrity error: {str(e)}")
        except SQLAlchemyError as e:
            self.session.rollback()
            raise TechnologyDatabaseError(f"Failed to add technology: {str(e)}")
