from database.models import Technology
from domain.technology.exceptions import TechnologyError
from domain.technology.technology_models import Technology_Create
from domain.technology.technology_repo import TechnologyRepo


class TechnologyService:
    def __init__(self, repo: TechnologyRepo) -> None:
        self.repo = repo

    def get_technologies(self) -> list[Technology]:
        """Get all technologies.

        Returns:
            list[Technology]: List of all technologies

        Raises:
            TechnologyError: If operation fails with a known error
            Exception: If an unexpected error occurs
        """
        try:
            return self.repo.get_technologies()
        except TechnologyError as e:
            raise e
        except Exception as e:
            raise Exception(f"Unexpected error in technology service: {str(e)}")

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
