from database.models import Project
from database.session import SessionDep
from domain.project.project_exceptions import ProjectDatabaseError, ProjectNotFoundError
from domain.project.project_schema import ProjectCreate, ProjectUpdate
from fastapi import status
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlmodel import select


class ProjectRepo:
    def __init__(self, session: SessionDep):
        """Initialize the Project repository.

        Args:
            session (SessionDep): Database session dependency
        """
        self.session = session

    async def get_projects(self) -> list[Project]:
        """Get all projects sorted by last entry date and name.

        Returns:
            list[Project]: List of all projects

        Raises:
            ProjectDatabaseError: If database operation fails
        """
        try:
            statement = select(Project).order_by(
                Project.last_entry_date.desc().nulls_last(), Project.name
            )
            results = await self.session.exec(statement)
            return results.all()

        except SQLAlchemyError as e:
            raise ProjectDatabaseError(message=f"Failed to fetch projects: {str(e)}")

    async def get_project(self, id: str) -> Project:
        """Get a single project by ID.

        Args:
            id (str): Project ID

        Returns:
            Project: The requested project

        Raises:
            ProjectDatabaseError: If project not found or database operation fails
        """
        try:
            found_project = await self.session.get(Project, id)
            if not found_project:
                raise ProjectNotFoundError(
                    message=f"Project with ID '{id}' not found",
                    status_code=status.HTTP_404_NOT_FOUND,
                )
            return found_project
        except SQLAlchemyError as e:
            raise ProjectDatabaseError(message=f"Failed to fetch project: {str(e)}")

    async def add_project(self, project: ProjectCreate) -> Project:
        """Add a new project to the database.

        Args:
            project (ProjectCreate): Project creation data

        Returns:
            Project: The newly created project

        Raises:
            ProjectDatabaseError: If database operation fails or project name already exists
        """
        try:
            db_project = Project.model_validate(project)
            return await self._save_project(db_project)
        except IntegrityError:
            await self.session.rollback()
            raise ProjectDatabaseError(
                message=f"Project name already exists: {project.name}",
                status_code=status.HTTP_409_CONFLICT,
            )
        except SQLAlchemyError as e:
            await self.session.rollback()
            raise ProjectDatabaseError(message=f"Failed to add project: {str(e)}")

    async def update_project(self, id: str, project: ProjectUpdate) -> Project:
        """Update an existing project.

        Args:
            id (str): Project ID
            project (ProjectUpdate): Project update data

        Returns:
            Project: The updated project

        Raises:
            ProjectDatabaseError: If project not found, database operation fails, or project name already exists
        """
        try:
            db_project = await self.get_project(id)
            # Update project data excluding None values
            project_data = project.model_dump(exclude_unset=True)
            for key, value in project_data.items():
                setattr(db_project, key, value)

            return await self._save_project(db_project)
        except ProjectDatabaseError as e:
            raise e
        except SQLAlchemyError as e:
            await self.session.rollback()
            raise ProjectDatabaseError(message=f"Failed to update project: {str(e)}")

    async def delete_project(self, id: str):
        """Delete a project by ID.

        Args:
            id (str): Project ID

        Raises:
            ProjectDatabaseError: If project has associated journal entries or database operation fails
        """
        try:
            async with self.session.begin():
                project = await self.get_project(id)
                has_journal_entries = len(project.journal_entries) > 0
                if has_journal_entries:
                    raise ProjectDatabaseError(
                        message=f"Project '{project.name}' cannot be deleted because it is used in journal entries",
                        status_code=status.HTTP_400_BAD_REQUEST,
                    )
                await self.session.delete(project)
        except SQLAlchemyError as e:
            raise ProjectDatabaseError(
                message=f"Failed to delete project: {str(e)}",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    async def _save_project(self, project: Project) -> Project:
        """Save project to database and refresh.

        Args:
            project: Project instance to save

        Returns:
            Project: Refreshed project instance

        Raises:
            SQLAlchemyError: If database operation fails
        """
        self.session.add(project)
        await self.session.commit()
        await self.session.refresh(project)
        return project
