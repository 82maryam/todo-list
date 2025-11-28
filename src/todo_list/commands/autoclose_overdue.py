from datetime import datetime

from sqlalchemy.orm import Session

from ..db.session import SessionLocal
from ..repositories.project_repository import ProjectRepository
from ..repositories.task_repository import TaskRepository
from ..services.task_service import TaskService


def run(now: datetime | None = None) -> int:
    if now is None:
        now = datetime.utcnow()

    session: Session = SessionLocal()
    try:
        project_repo = ProjectRepository(session)
        task_repo = TaskRepository(session)
        task_service = TaskService(
            task_repository=task_repo,
            project_repository=project_repo,
        )

        updated_count = task_service.close_overdue_tasks(now=now)
        return updated_count
    finally:
        session.close()


def main() -> None:
    print("Running auto-close for overdue tasks...")
    try:
        count = run()
        print(f"Auto-close completed. Updated {count} task(s).")
    except Exception as exc:
        print(f"Error while auto-closing overdue tasks: {exc}")
