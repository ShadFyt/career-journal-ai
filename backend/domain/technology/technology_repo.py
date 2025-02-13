from database.models import JournalEntryTechnologyLink, Technology
from database.session import SessionDep
from domain.technology.exceptions import (
    TechnologyDatabaseError,
    TechnologyNotFoundError,
)
from domain.technology.technology_models import Technology_Create, TechnologyWithCount
from enums import Language
from fastapi import status
from sqlalchemy import func, label, text
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
            list[TechnologyWithCount]: List of  all technologies with their usage counts

        Raises:
            TechnologyDatabaseError: If database operation fails
        """
        try:
            usage_count = self._build_usage_count_subquery()
            query = self._build_base_query(usage_count)
            query = self._apply_filters(query, language)

            results = self.session.exec(query).all()
            return self._map_to_domain(results)

        except SQLAlchemyError as e:
            raise TechnologyDatabaseError(f"Failed to fetch technologies: {str(e)}")

    def get_technology(self, id: str) -> Technology:
        """Get a technology from the database by its ID.

        Args:
            id: Unique identifier of the technology to retrieve

        Raises:
            TechnologyNotFoundError: If technology with given ID does not exist
            TechnologyDatabaseError: If database operation fails
        """
        try:
            foundTechnology = self.session.get(Technology, id)
            if not foundTechnology:
                raise TechnologyNotFoundError(status_code=status.HTTP_404_NOT_FOUND)
            return foundTechnology
        except SQLAlchemyError as e:
            raise TechnologyDatabaseError(f"Failed to fetch technology: {str(e)}")

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

    def delete_technology(self, id: str):
        """Delete a technology from the database by its ID.

        Args:
            id: Unique identifier of the technology to delete

        Raises:
            TechnologyNotFoundError: If technology with given ID does not exist
            TechnologyDatabaseError: If technology is referenced by journal entries
                or if database operation fails
        """
        try:
            technology = self.get_technology(id)
            has_journal_entries = len(technology.journal_entries) > 0
            if has_journal_entries:
                raise TechnologyDatabaseError(
                    f"Technology '{technology.name}' cannot be deleted because it is used in journal entries",
                    status_code=status.HTTP_400_BAD_REQUEST,
                )
            self.session.delete(technology)
            self.session.commit()
        except SQLAlchemyError as e:
            self.session.rollback()
            raise TechnologyDatabaseError(f"Failed to delete technology: {str(e)}")

    def _build_usage_count_subquery(self):
        """Build a subquery to count technology usage in journal entries.

        Returns:
            Label: SQLAlchemy label for the usage count subquery
        """
        return (
            select(func.count(JournalEntryTechnologyLink.journal_entry_id))
            .where(JournalEntryTechnologyLink.technology_id == Technology.id)
            .scalar_subquery()
            .label("usage_count")
        )

    def _build_base_query(self, usage_count: label) -> select:
        """Build the base query for fetching technologies with their counts.

        Args:
            usage_count: The usage count subquery label

        Returns:
            Select: Base SQLAlchemy select statement
        """
        return select(
            Technology.id,
            Technology.name,
            Technology.description,
            Technology.language,
            usage_count,
        )

    def _apply_filters(self, query: select, language: Language | None) -> select:
        """Apply filters to the technology query.

        Args:
            query: Base SQLAlchemy select statement
            language: Optional language filter

        Returns:
            Select: Filtered SQLAlchemy select statement
        """
        if language is not None:
            query = query.where(Technology.language == language)
        return query.order_by(
            Technology.language, Technology.name, text("usage_count DESC")
        )

    def _map_to_domain(self, results: list[tuple]) -> list[TechnologyWithCount]:
        """Map database results to domain objects.

        Args:
            results: List of database result tuples

        Returns:
            list[TechnologyWithCount]: List of domain objects
        """
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
