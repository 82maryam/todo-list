from dotenv import load_dotenv
from sqlalchemy.orm import Session

from .cli.interface import CLIInterface
from .db.session import SessionLocal
from .repositories.project_repository import ProjectRepository
from .repositories.task_repository import TaskRepository
from .services import ProjectService, TaskService


def main() -> None:
    load_dotenv()

    session: Session = SessionLocal()
    try:
        project_repo = ProjectRepository(session)
        task_repo = TaskRepository(session)

        project_service = ProjectService(project_repository=project_repo)
        task_service = TaskService(
            task_repository=task_repo,
            project_repository=project_repo,
        )

        cli = CLIInterface(
            project_service=project_service,
            task_service=task_service,
        )

        cli.run()
    except KeyboardInterrupt:
        print("\n\nExiting...")
    except Exception as e:
        print(f"Unexpected error: {e}")
    finally:
        session.close()


if __name__ == "__main__":
    main()
