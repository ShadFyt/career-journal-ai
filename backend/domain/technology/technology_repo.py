import asyncio
from logging import getLogger

from database.models import JournalEntryTechnologyLink, Technology
from database.session import SessionDep
from domain.technology.technology_exceptions import (
    ErrorCode,
    TechnologyDatabaseError,
    TechnologyNotFoundError,
)
from domain.technology.technology_schema import (
    TechnologyCreate,
    TechnologyWithCount,
    TechnologyUpdate,
)

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

    @staticmethod
    def _build_base_query(usage_count, user_id: str):
        """Build the base query for retrieving technologies with usage counts."""
        return (
            select(
                Technology,
                label("usage_count", func.coalesce(usage_count.c.usage_count, 0)),
            )
            .where(Technology.user_id == user_id)
            .outerjoin(
                usage_count,
                Technology.id == usage_count.c.technology_id,
            )
            .order_by(text("usage_count DESC"), Technology.name)
        )

    async def get_technologies(
        self, user_id: str, language: Language | None = None
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
            query = self._build_base_query(usage_count, user_id)
            query = self._apply_filters(query, language)

            results = await self.session.exec(query)
            return self._map_to_domain(results.all())

        except SQLAlchemyError as e:
            raise TechnologyDatabaseError(
                code=ErrorCode.DATABASE_ERROR,
                message="Failed to fetch technologies",
                params={"error": str(e)},
            )

    async def get_technology(self, tech_id: str) -> Technology:
        """Get a technology from the database by its ID.

        Args:
            tech_id: Unique identifier of the technology to retrieve

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
                .where(Technology.id == tech_id)
            )
            result = await self.session.exec(statement)
            technology = result.first()
            if not technology:
                raise TechnologyNotFoundError(
                    code=ErrorCode.TECHNOLOGY_NOT_FOUND,
                    message="Technology not found",
                    params={"id": tech_id},
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

    async def add_technology(
        self, technology: TechnologyCreate, user_id: str
    ) -> Technology:
        """Add a new technology to the database.

        Args:
            technology: Technology data to add
            user_id: Unique identifier of the user who created the technology

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
                user_id=user_id,
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

    async def delete_technology(self, tech_id: str) -> None:
        """Delete a technology from the database.

        Args:
            tech_id: Unique identifier of the technology to delete

        Raises:
            TechnologyNotFoundError: If technology with given ID does not exist
            TechnologyDatabaseError: If database operation fails or technology has journal entries
        """
        try:
            technology = await self.get_technology(tech_id)
            has_journal_entries = len(technology.journal_entries) > 0
            if has_journal_entries:
                raise TechnologyDatabaseError(
                    code=ErrorCode.INVALID_OPERATION,
                    message="Cannot delete technology that is referenced by journal entries",
                    params={
                        "id": tech_id,
                        "usage_count": len(technology.journal_entries),
                    },
                    status_code=status.HTTP_409_CONFLICT,
                )

            await asyncio.shield(self.session.delete(technology))
            await asyncio.shield(self.session.commit())
            logger.info(f"Deleted technology with id {tech_id}")

        except SQLAlchemyError as e:
            await self.session.rollback()
            logger.error(f"Failed to delete technology with id {tech_id}: {str(e)}")
            raise TechnologyDatabaseError(
                code=ErrorCode.DATABASE_ERROR,
                message="Failed to delete technology",
                params={"error": str(e)},
            )

    async def update_technology(
        self, tech_id: str, technology_data: TechnologyUpdate
    ) -> Technology:
        """Update an existing technology in the database.

        Args:
            tech_id: Unique identifier of the technology to update
            technology_data: Pydantic model with fields to update

        Returns:
            Technology: The updated technology

        Raises:
            TechnologyNotFoundError: If technology with given ID does not exist
            TechnologyDatabaseError: If database operation fails or integrity constraint is violated
        """
        try:
            # First check if the technology exists
            technology = await self.get_technology(tech_id)

            # Get dictionary of fields explicitly set in the request
            update_data = technology_data.model_dump(exclude_unset=True)

            # Update only the provided fields
            updated = False
            for key, value in update_data.items():
                if getattr(technology, key) != value:
                    setattr(technology, key, value)  # Update attributes dynamically
                    updated = True

            # Commit the changes only if something actually changed
            if updated:
                self.session.add(
                    technology
                )  # Add the modified object back to the session context
                await self.session.commit()
                await self.session.refresh(technology)
                logger.info(f"Updated technology with id {tech_id}")
            else:
                logger.info(f"No updates needed for technology with id {tech_id}")

            return technology

        except IntegrityError as e:
            await self.session.rollback()
            # Use .get() for safer access in the error message, provide default if name wasn't in update
            updated_name = technology_data.model_dump().get("name", technology.name)
            if "unique constraint" in str(e).lower():
                raise TechnologyDatabaseError(
                    code=ErrorCode.DUPLICATE_TECHNOLOGY,
                    message="Technology with this name already exists",
                    params={"name": updated_name},  # Use the potentially updated name
                    status_code=status.HTTP_409_CONFLICT,
                )
            raise TechnologyDatabaseError(
                code=ErrorCode.DATABASE_ERROR,
                message="Failed to update technology due to integrity error",
                params={"error": str(e)},
            )

        except SQLAlchemyError as e:
            await self.session.rollback()
            logger.error(f"Failed to update technology with id {tech_id}: {str(e)}")
            raise TechnologyDatabaseError(
                code=ErrorCode.DATABASE_ERROR,
                message="Failed to update technology",
                params={"error": str(e)},
            )

    @staticmethod
    def _build_usage_count_subquery():
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

    @staticmethod
    def _apply_filters(query, language: Language | None):
        """Apply filters to the query."""
        if language:
            query = query.filter(Technology.language == language)
        return query

    @staticmethod
    def _map_to_domain(results) -> list[TechnologyWithCount]:
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
