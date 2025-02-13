from database.session import SessionDep
from domain.project.exceptions import ProjectDatabaseError
from domain.project.project import Project
from domain.project.project_models import Project_Create
from fastapi import status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, SQLAlchemyError


class ProjectRepo:
    def __init__(self, session: SessionDep):
        self.session = session

    def get_projects(self) -> list[Project]:
        try:
            statement = select(Project).order_by(
                Project.last_entry_date.desc(), Project.name
            )
            return self.session.exec(statement).all()
        except SQLAlchemyError as e:
            raise ProjectDatabaseError(f"Failed to fetch projects: {str(e)}")

    def get_project(self, id: str) -> Project:
        try:
            found_project = self.session.get(Project, id)
            if not found_project:
                raise ProjectDatabaseError(
                    f"Project with ID '{id}' not found",
                    status_code=status.HTTP_404_NOT_FOUND,
                )
            return found_project
        except SQLAlchemyError as e:
            raise ProjectDatabaseError(f"Failed to fetch project: {str(e)}")

    def add_project(self, project: Project_Create) -> Project:
        try:
            db_project = Project(**project.model_dump())
            self.session.add(db_project)
            self.session.commit()
            self.session.refresh(db_project)
            return db_project
        except IntegrityError as e:
            self.session.rollback()
            if "UNIQUE constraint failed" in str(e.orig):
                raise ProjectDatabaseError(
                    f"Project with name '{project.name}' already exists",
                    status_code=status.HTTP_400_BAD_REQUEST,
                )
            raise ProjectDatabaseError(f"Database integrity error: {str(e)}")
        except SQLAlchemyError as e:
            self.session.rollback()
            raise ProjectDatabaseError(f"Failed to add project: {str(e)}")

    def delete_project(self, id: str):
        try:
            project = self.get_project(id)
            has_journal_entries = len(project.journal_entries) > 0
            if has_journal_entries:
                raise ProjectDatabaseError(
                    f"Project '{project.name}' cannot be deleted because it is used in journal entries",
                    status_code=status.HTTP_400_BAD_REQUEST,
                )
            self.session.delete(project)
            self.session.commit()
        except SQLAlchemyError as e:
            self.session.rollback()
            raise ProjectDatabaseError(f"Failed to delete project: {str(e)}")
