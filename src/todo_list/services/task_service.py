import os
from datetime import datetime, date
from typing import List, Optional

from ..core.exceptions import (
    ValidationError,
    LimitExceededError,
    NotFoundError,
)
from ..core.validators import Validator
from ..models.task import Task
from ..repositories.project_repository import ProjectRepository
from ..repositories.task_repository import TaskRepository


class TaskService:

    ALLOWED_STATUSES = {"todo", "doing", "done"}

    def __init__(
        self,
        task_repository: TaskRepository,
        project_repository: ProjectRepository,
        max_tasks_per_project: Optional[int] = None,
    ) -> None:
        self._task_repository = task_repository
        self._project_repository = project_repository

        if max_tasks_per_project is None:
            max_tasks_env = os.getenv("MAX_NUMBER_OF_TASKS", "1000")
            try:
                max_tasks_per_project = int(max_tasks_env)
            except ValueError:
                raise ValidationError(
                    "MAX_NUMBER_OF_TASKS must be an integer"
                )
        self._max_tasks_per_project = max_tasks_per_project

    def _validate_status(self, status: str) -> str:
        if status not in self.ALLOWED_STATUSES:
            allowed = ", ".join(sorted(self.ALLOWED_STATUSES))
            raise ValidationError(
                f"Invalid status '{status}'. Allowed values: {allowed}"
            )
        return status

    def _parse_deadline(self, deadline: Optional[str]) -> Optional[date]:
        if deadline is None:
            return None

        Validator.validate_deadline(deadline)
        return date.fromisoformat(deadline)


    def create_task(
        self,
        project_id: int,
        title: str,
        description: str,
        *,
        status: str = "todo",
        deadline: Optional[str] = None,
    ) -> Task:

        self._project_repository.get_by_id(project_id)

        title = Validator.validate_text(title, "Task title", 30)
        description = Validator.validate_text(
            description, "Task description", 150
        )

        status = self._validate_status(status)
        deadline_date = self._parse_deadline(deadline)

        existing_tasks = self._task_repository.list_by_project(project_id)
        if len(existing_tasks) >= self._max_tasks_per_project:
            raise LimitExceededError(
                f"Cannot create more than {self._max_tasks_per_project} "
                f"tasks for project {project_id}"
            )

        task = self._task_repository.create(
            project_id=project_id,
            title=title,
            description=description,
            status=status,
            deadline=deadline_date,
        )
        return task

    def list_tasks_for_project(self, project_id: int) -> List[Task]:
        # اگر پروژه وجود نداشته باشد، ارور NotFoundError بدهیم
        self._project_repository.get_by_id(project_id)
        return self._task_repository.list_by_project(project_id)

    def get_task(self, task_id: int) -> Task:
        return self._task_repository.get_by_id(task_id)

    def update_task(
        self,
        task_id: int,
        *,
        title: Optional[str] = None,
        description: Optional[str] = None,
        status: Optional[str] = None,
        deadline: Optional[str] = None,
    ) -> Task:
        task = self._task_repository.get_by_id(task_id)

        if title is not None:
            task.title = Validator.validate_text(
                title, "Task title", 30
            )

        if description is not None:
            task.description = Validator.validate_text(
                description, "Task description", 150
            )

        if status is not None:
            task.status = self._validate_status(status)

        if deadline is not None:
            task.deadline = self._parse_deadline(deadline)

        updated = self._task_repository.save(task)
        return updated

    def change_status(self, task_id: int, status: str) -> Task:
        status = self._validate_status(status)
        task = self._task_repository.get_by_id(task_id)
        task.status = status
        return self._task_repository.save(task)

    def delete_task(self, task_id: int) -> None:
        self._task_repository.delete(task_id)

    def close_overdue_tasks(self, now: Optional[datetime] = None) -> int:
        if now is None:
            now = datetime.utcnow()

        overdue_tasks = self._task_repository.get_overdue_tasks(now)
        if not overdue_tasks:
            return 0

        for task in overdue_tasks:
            task.status = "done"
            task.closed_at = now
            self._task_repository.save(task)

        return len(overdue_tasks)
