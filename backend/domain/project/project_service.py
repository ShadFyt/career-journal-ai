from database.models import Project
from domain.project.project_repo import ProjectRepo
from domain.project.project_schema import ProjectCreate, ProjectUpdate


class ProjectService:
    def __init__(self, repo: ProjectRepo) -> None:
        self.repo = repo

    def get_projects(self) -> list[Project]:
        """Get all projects and convert to DTOs."""
        projects = self.repo.get_projects()
        return projects

    def get_project(self, id: str) -> Project:
        """Get a single project and convert to DTO."""
        return self.repo.get_project(id)

    def add_project(self, project: ProjectCreate) -> Project:
        """Add a project and convert result to DTO."""
        return self.repo.add_project(project)

    def delete_project(self, id: str) -> None:
        """Delete a project."""
        return self.repo.delete_project(id)

    def update_project(self, id: str, project: ProjectUpdate) -> Project:
        """Update an existing project and convert result to DTO."""
        return self.repo.update_project(id, project)
