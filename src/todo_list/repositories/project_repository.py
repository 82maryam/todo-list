from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from ..core.exceptions import NotFoundError, DuplicateError
from ..models.project import Project
from .base import SqlAlchemyRepository


class ProjectRepository(SqlAlchemyRepository):

    def __init__(self, session: Session) -> None:
        super().__init__(session)

    def create(self, name: str, description: str) -> Project:
        existing = self.get_by_name(name)
        if existing is not None:
            raise DuplicateError(f"Project with name '{name}' already exists")

        project = Project(name=name, description=description)
        self._session.add(project)
        self._session.commit()
        self._session.refresh(project)
        return project

    def get_by_id(self, project_id: int) -> Project:
        project = self._session.get(Project, project_id)
        if project is None:
            raise NotFoundError(f"Project with id {project_id} not found")
        return project

    def get_by_name(self, name: str) -> Optional[Project]:
        stmt = select(Project).where(Project.name == name)
        result = self._session.execute(stmt).scalar_one_or_none()
        return result

    def list_all(self) -> List[Project]:
        stmt = select(Project).order_by(Project.created_at.asc())
        result = self._session.execute(stmt).scalars().all()
        return list(result)

    def update(
        self,
        project_id: int,
        *,
        name: Optional[str] = None,
        description: Optional[str] = None,
    ) -> Project:
        project = self.get_by_id(project_id)

        if name is not None and name != project.name:
            existing = self.get_by_name(name)
            if existing is not None and existing.id != project.id:
                raise DuplicateError(f"Project with name '{name}' already exists")
            project.name = name

        if description is not None:
            project.description = description

        self._session.commit()
        self._session.refresh(project)
        return project

    def delete(self, project_id: int) -> None:
        project = self.get_by_id(project_id)
        self._session.delete(project)
        self._session.commit()
