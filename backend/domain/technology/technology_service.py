from core.exceptions import BaseDomainError
from database.models import Technology
from domain.technology.technology_exceptions import TechnologyNotFoundError
from domain.technology.technology_repo import TechnologyRepo
from domain.technology.technology_schema import Technology_Create, TechnologyWithCount
from enums import Language


class TechnologyService:
    def __init__(self, repo: TechnologyRepo) -> None:
        self.repo = repo

    async def get_technologies(
        self, user_id: str, language: Language | None = None
    ) -> list[TechnologyWithCount]:
        """Get all technologies with their usage counts.

        Args:
            language: Optional filter by programming language
            user_id: Unique identifier of the user

        Returns:
            list[TechnologyWithCount]: List of technologies with their usage counts

        Raises:
            TechnologyError: If database operation fails
        """
        return await self.repo.get_technologies(language=language, user_id=user_id)

    async def get_technologies_by_ids(self, ids: list[str]) -> list[Technology]:
        """Get technologies by their IDs.

        Args:
            ids: List of technology IDs

        Returns:
            list[Technology]: List of technologies

        Raises:
            TechnologyNotFoundError: If not all technologies found
        """
        technologies = await self.repo.get_technologies_by_ids(ids)

        if len(technologies) != len(ids):
            raise TechnologyNotFoundError(message="Not all technologies found")

        return technologies

    async def add_technology(self, technology: Technology_Create) -> Technology:
        """Create a new technology.

        Returns:
            Technology: The newly created technology

        Raises:
            TechnologyError: If operation fails with a known error
            Exception: If an unexpected error occurs
        """
        try:
            return await self.repo.add_technology(technology)
        except BaseDomainError as e:
            raise e
        except Exception as e:
            raise Exception(f"Unexpected error in technology service: {str(e)}")

    async def delete_technology(self, id: str):
        """Delete a technology from the database by its ID.

        Args:
            id: Unique identifier of the technology to delete

        Raises:
            TechnologyNotFoundError: If technology with given ID does not exist
            TechnologyDatabaseError: If technology is referenced by journal entries
                or if database operation fails
        """
        try:
            await self.repo.delete_technology(id)
        except BaseDomainError as e:
            raise e
        except Exception as e:
            raise Exception(f"Unexpected error in technology service: {str(e)}")
