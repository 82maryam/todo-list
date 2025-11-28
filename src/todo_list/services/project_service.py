import os
from typing import List, Optional

from ..core.exceptions import (
    ValidationError,
    LimitExceededError,
    NotFoundError,
    DuplicateError,
)
from ..core.validators import Validator
from ..models.project import Project
from ..repositories.project_repository import ProjectRepository


class ProjectService:

    def __init__(
        self,
        project_repository: ProjectRepository,
        max_projects: Optional[int] = None,
    ) -> None:
        self._project_repository = project_repository
        if max_projects is None:
            max_projects_env = os.getenv("MAX_NUMBER_OF_PROJECTS", "100")
            try:
                max_projects = int(max_projects_env)
            except ValueError:
                raise ValidationError(
                    "MAX_NUMBER_OF_PROJECTS must be an integer"
                )
        self._max_projects = max_projects


    def create_project(self, name: str, description: str) -> Project:
        name = Validator.validate_text(name, "Project name", 30)
        description = Validator.validate_text(
            description, "Project description", 150
        )

        existing_projects = self._project_repository.list_all()
        if len(existing_projects) >= self._max_projects:
            raise LimitExceededError(
                f"Cannot create more than {self._max_projects} projects"
            )

        try:
            return self._project_repository.create(
                name=name,
                description=description,
            )
        except DuplicateError:
            raise

    def list_projects(self) -> List[Project]:
        return self._project_repository.list_all()

    def get_project(self, project_id: int) -> Project:
        return self._project_repository.get_by_id(project_id)

    def update_project(
        self,
        project_id: int,
        *,
        name: Optional[str] = None,
        description: Optional[str] = None,
    ) -> Project:
        if name is not None:
            name = Validator.validate_text(name, "Project name", 30)
        if description is not None:
            description = Validator.validate_text(
                description, "Project description", 150
            )

        try:
            return self._project_repository.update(
                project_id=project_id,
                name=name,
                description=description,
            )
        except NotFoundError:
            raise
        except DuplicateError:
            raise

    def delete_project(self, project_id: int) -> None:
        self._project_repository.delete(project_id)
