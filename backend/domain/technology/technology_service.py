from database.models import Technology
from domain.technology.technology_repo import TechnologyRepo


class TechnologyService:
    def __init__(self, repo: TechnologyRepo) -> None:
        self.repo = repo

    def get_technologies(self) -> list[Technology]:
        return self.repo.get_technologies()
