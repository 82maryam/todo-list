from collections.abc import Generator

from sqlalchemy.orm import Session

from ..db.session import SessionLocal
from ..repositories.project_repository import ProjectRepository
from ..repositories.task_repository import TaskRepository
from ..services.project_service import ProjectService
from ..services.task_service import TaskService


def get_db_session() -> Generator[Session, None, None]:
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_project_service(db: Session) -> ProjectService:
    project_repo = ProjectRepository(db)
    return ProjectService(project_repository=project_repo)


def get_task_service(db: Session) -> TaskService:
    project_repo = ProjectRepository(db)
    task_repo = TaskRepository(db)
    return TaskService(
        task_repository=task_repo,
        project_repository=project_repo,
    )
