from database.models import Project
from domain.project.project_repo import ProjectRepo
from domain.project.project_schema import ProjectCreate, ProjectUpdate


class ProjectService:
    def __init__(self, repo: ProjectRepo) -> None:
        self.repo = repo

    async def get_projects(self) -> list[Project]:
        """Get all projects and convert to DTOs."""
        projects = await self.repo.get_projects()
        return projects

    async def get_project(self, id: str) -> Project:
        """Get a single project and convert to DTO."""
        return await self.repo.get_project(id)

    async def add_project(self, project: ProjectCreate) -> Project:
        """Add a project and convert result to DTO."""
        return await self.repo.add_project(project)

    async def delete_project(self, id: str) -> None:
        """Delete a project."""
        await self.repo.delete_project(id)

    async def update_project(self, id: str, project: ProjectUpdate) -> Project:
        """Update an existing project and convert result to DTO."""
        return await self.repo.update_project(id, project)
