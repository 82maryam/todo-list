from datetime import datetime, date
from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from ..core.exceptions import NotFoundError
from ..models.task import Task
from .base import SqlAlchemyRepository


class TaskRepository(SqlAlchemyRepository):

    def __init__(self, session: Session) -> None:
        super().__init__(session)

    def create(
        self,
        project_id: int,
        title: str,
        description: str,
        *,
        status: str = "todo",
        deadline: Optional[date] = None,
    ) -> Task:
        task = Task(
            project_id=project_id,
            title=title,
            description=description,
            status=status,
            deadline=deadline,
        )
        self._session.add(task)
        self._session.commit()
        self._session.refresh(task)
        return task

    def get_by_id(self, task_id: int) -> Task:
        task = self._session.get(Task, task_id)
        if task is None:
            raise NotFoundError(f"Task with id {task_id} not found")
        return task

    def list_by_project(self, project_id: int) -> List[Task]:
        stmt = (
            select(Task)
            .where(Task.project_id == project_id)
            .order_by(Task.created_at.asc())
        )
        result = self._session.execute(stmt).scalars().all()
        return list(result)

    def save(self, task: Task) -> Task:
        self._session.add(task)
        self._session.commit()
        self._session.refresh(task)
        return task

    def delete(self, task_id: int) -> None:
        task = self.get_by_id(task_id)
        self._session.delete(task)
        self._session.commit()

    def get_overdue_tasks(self, now: datetime) -> List[Task]:
        today = now.date()
        stmt = (
            select(Task)
            .where(
                Task.deadline.is_not(None),
                Task.deadline < today,
                Task.status != "done",
            )
            .order_by(Task.deadline.asc())
        )
        result = self._session.execute(stmt).scalars().all()
        return list(result)
