from database.models import Technology, JournalEntryTechnologyLink
from database.session import SessionDep
from domain.technology.exceptions import TechnologyDatabaseError
from domain.technology.technology_models import Technology_Create, TechnologyWithCount
from enums import Language
from fastapi import status
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlmodel import select


class TechnologyRepo:
    def __init__(self, session: SessionDep):
        self.session = session

    def get_technologies(
        self, language: Language | None = None
    ) -> list[TechnologyWithCount]:
        """Get all technologies from the database with their usage counts.

        Args:
            language: Optional filter by programming language

        Returns:
            list[TechnologyWithCount]: List of all technologies with their usage counts

        Raises:
            TechnologyDatabaseError: If database operation fails
        """
        try:
            # Create a subquery to count journal entries
            usage_count = (
                select(func.count(JournalEntryTechnologyLink.journal_entry_id))
                .where(JournalEntryTechnologyLink.technology_id == Technology.id)
                .scalar_subquery()
                .label("usage_count")
            )

            # Base query with the count
            statement = select(
                Technology.id,
                Technology.name,
                Technology.description,
                Technology.language,
                usage_count,
            )

            # Apply language filter if provided
            if language is not None:
                statement = statement.where(Technology.language == language)

            # Order by language, name, and usage count
            statement = statement.order_by(
                Technology.language, Technology.name, usage_count.desc()
            )

            results = self.session.exec(statement).all()

            # Convert results to TechnologyWithCount objects
            return [
                TechnologyWithCount(
                    id=id_,
                    name=name,
                    description=description,
                    language=language,
                    usage_count=count or 0,
                )
                for id_, name, description, language, count in results
            ]
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
