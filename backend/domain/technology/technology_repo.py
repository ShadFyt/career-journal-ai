import asyncio
from logging import getLogger

from database.models import JournalEntryTechnologyLink, Technology
from database.session import SessionDep
from domain.technology.technology_exceptions import (
    ErrorCode,
    TechnologyDatabaseError,
    TechnologyNotFoundError,
)
from domain.technology.technology_schema import Technology_Create, TechnologyWithCount
from enums import Language
from fastapi import status
from sqlalchemy import func, label, text
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import selectinload
from sqlmodel import select

logger = getLogger(__name__)


class TechnologyRepo:
    def __init__(self, session: SessionDep):
        self.session = session

    async def get_technologies(
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

            results = await self.session.exec(query)
            return self._map_to_domain(results.all())

        except SQLAlchemyError as e:
            raise TechnologyDatabaseError(
                code=ErrorCode.DATABASE_ERROR,
                message="Failed to fetch technologies",
                params={"error": str(e)},
            )

    async def get_technology(self, id: str) -> Technology:
        """Get a technology from the database by its ID.

        Args:
            id: Unique identifier of the technology to retrieve

        Returns:
            Technology: The requested technology

        Raises:
            TechnologyNotFoundError: If technology with given ID does not exist
            TechnologyDatabaseError: If database operation fails
        """
        try:
            statement = (
                select(Technology)
                .options(selectinload(Technology.journal_entries))
                .where(Technology.id == id)
            )
            result = await self.session.exec(statement)
            technology = result.first()
            if not technology:
                raise TechnologyNotFoundError(
                    code=ErrorCode.TECHNOLOGY_NOT_FOUND,
                    message="Technology not found",
                    params={"id": id},
                )
            return technology

        except SQLAlchemyError as e:
            raise TechnologyDatabaseError(
                code=ErrorCode.DATABASE_ERROR,
                message="Failed to fetch technology",
                params={"error": str(e)},
            )

    async def get_technologies_by_ids(self, ids: list[str]) -> list[Technology]:
        """Get technologies by their IDs.

        Args:
            ids: List of technology IDs

        Returns:
            list[Technology]: List of technologies

        Raises:
            TechnologyDatabaseError: If database operation fails
        """
        try:
            query = select(Technology).where(Technology.id.in_(ids))
            results = await self.session.exec(query)
            return results.all()

        except SQLAlchemyError as e:
            raise TechnologyDatabaseError(
                code=ErrorCode.DATABASE_ERROR,
                message="Failed to fetch technologies",
                params={"error": str(e)},
            )

    async def add_technology(self, technology: Technology_Create) -> Technology:
        """Add a new technology to the database.

        Args:
            technology: Technology data to add

        Returns:
            Technology: The newly created technology

        Raises:
            TechnologyDatabaseError: If database operation fails or technology with same name exists
        """
        try:
            new_technology = Technology(
                name=technology.name,
                description=technology.description,
                language=technology.language,
            )
            self.session.add(new_technology)
            await self.session.commit()
            await self.session.refresh(new_technology)
            return new_technology

        except IntegrityError as e:
            await self.session.rollback()
            if "unique constraint" in str(e).lower():
                raise TechnologyDatabaseError(
                    code=ErrorCode.DUPLICATE_TECHNOLOGY,
                    message="Technology with this name already exists",
                    params={"name": technology.name},
                    status_code=status.HTTP_409_CONFLICT,
                )
            raise TechnologyDatabaseError(
                code=ErrorCode.DATABASE_ERROR,
                message="Failed to add technology",
                params={"error": str(e)},
            )

        except SQLAlchemyError as e:
            await self.session.rollback()
            raise TechnologyDatabaseError(
                code=ErrorCode.DATABASE_ERROR,
                message="Failed to add technology",
                params={"error": str(e)},
            )

    async def delete_technology(self, id: str) -> None:
        """Delete a technology from the database.

        Args:
            id: Unique identifier of the technology to delete

        Raises:
            TechnologyNotFoundError: If technology with given ID does not exist
            TechnologyDatabaseError: If database operation fails or technology has journal entries
        """
        try:
            technology = await self.get_technology(id)
            has_journal_entries = len(technology.journal_entries) > 0
            if has_journal_entries:
                raise TechnologyDatabaseError(
                    code=ErrorCode.INVALID_OPERATION,
                    message="Cannot delete technology that is referenced by journal entries",
                    params={"id": id, "usage_count": len(technology.journal_entries)},
                    status_code=status.HTTP_409_CONFLICT,
                )

            await asyncio.shield(self.session.delete(technology))
            await asyncio.shield(self.session.commit())
            logger.info(f"Deleted technology with id {id}")

        except SQLAlchemyError as e:
            await self.session.rollback()
            logger.error(f"Failed to delete technology with id {id}: {str(e)}")
            raise TechnologyDatabaseError(
                code=ErrorCode.DATABASE_ERROR,
                message="Failed to delete technology",
                params={"error": str(e)},
            )

    def _build_usage_count_subquery(self):
        """Build a subquery to count technology usage in journal entries."""
        return (
            select(
                JournalEntryTechnologyLink.technology_id,
                func.count(JournalEntryTechnologyLink.journal_entry_id).label(
                    "usage_count"
                ),
            )
            .group_by(JournalEntryTechnologyLink.technology_id)
            .subquery()
        )

    def _build_base_query(self, usage_count):
        """Build the base query for retrieving technologies with usage counts."""
        return (
            select(
                Technology,
                label("usage_count", func.coalesce(usage_count.c.usage_count, 0)),
            )
            .outerjoin(
                usage_count,
                Technology.id == usage_count.c.technology_id,
            )
            .order_by(text("usage_count DESC"), Technology.name)
        )

    def _apply_filters(self, query, language: Language | None):
        """Apply filters to the query."""
        if language:
            query = query.filter(Technology.language == language)
        return query

    def _map_to_domain(self, results) -> list[TechnologyWithCount]:
        """Map database results to domain models."""
        return [
            TechnologyWithCount(
                id=tech.id,
                name=tech.name,
                description=tech.description,
                language=tech.language,
                usage_count=count,
            )
            for tech, count in results
        ]
