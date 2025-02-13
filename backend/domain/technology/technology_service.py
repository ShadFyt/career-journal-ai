from database.models import Technology
from domain.technology.exceptions import TechnologyError
from domain.technology.technology_models import Technology_Create, TechnologyWithCount
from domain.technology.technology_repo import TechnologyRepo
from enums import Language


class TechnologyService:
    def __init__(self, repo: TechnologyRepo) -> None:
        self.repo = repo

    def get_technologies(
        self, language: Language | None = None
    ) -> list[TechnologyWithCount]:
        """Get all technologies with their usage counts.

        Args:
            language: Optional filter by programming language

        Returns:
            list[TechnologyWithCount]: List of technologies with their usage counts

        Raises:
            TechnologyError: If database operation fails
        """
        return self.repo.get_technologies(language=language)

    def add_technology(self, technology: Technology_Create) -> Technology:
        """Create a new technology.

        Returns:
            Technology: The newly created technology

        Raises:
            TechnologyError: If operation fails with a known error
            Exception: If an unexpected error occurs
        """
        try:
            return self.repo.add_technology(technology)
        except TechnologyError as e:
            raise e
        except Exception as e:
            raise Exception(f"Unexpected error in technology service: {str(e)}")
