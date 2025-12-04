from typing import Optional

from ..core.exceptions import (
    TodoListError,
    ValidationError,
    DuplicateError,
    LimitExceededError,
    NotFoundError,
)
from ..services.project_service import ProjectService
from ..services.task_service import TaskService


class CLIInterface:

    def __init__(
        self,
        project_service: ProjectService,
        task_service: TaskService,
    ) -> None:
        self.project_service = project_service
        self.task_service = task_service
        self.running = True


    def get_user_input(self, prompt: str) -> str:
        while True:
            try:
                value = input(prompt).strip()
                if value == "":
                    print("Input cannot be empty. Please try again.")
                    continue
                return value
            except KeyboardInterrupt:
                print("\n\nExiting program...")
                self.running = False
                return ""
            except EOFError:
                print("\n\nExiting program...")
                self.running = False
                return ""

    def get_optional_input(self, prompt: str) -> Optional[str]:
        try:
            value = input(prompt).strip()
            return value or None
        except KeyboardInterrupt:
            print("\n\nExiting program...")
            self.running = False
            return None
        except EOFError:
            print("\n\nExiting program...")
            self.running = False
            return None

    def get_int_input(self, prompt: str) -> Optional[int]:
        while True:
            raw = self.get_user_input(prompt)
            if not self.running:
                return None
            try:
                return int(raw)
            except ValueError:
                print("Invalid number. Please enter a valid integer.")

    def handle_error(self, error: Exception) -> None:
        if isinstance(error, ValidationError):
            print(f"Validation error: {error}")
        elif isinstance(error, DuplicateError):
            print(f"Duplicate error: {error}")
        elif isinstance(error, LimitExceededError):
            print(f"Limit exceeded: {error}")
        elif isinstance(error, NotFoundError):
            print(f"Not found: {error}")
        elif isinstance(error, TodoListError):
            print(f"Application error: {error}")
        else:
            print(f"Unexpected error: {error}")

    def display_main_menu(self) -> None:
        print("\n" + "=" * 40)
        print(" ToDo List Application")
        print("=" * 40)
        print("1. Project management")
        print("2. Task management")
        print("3. Exit")
        print("-" * 40)

    def display_projects_menu(self) -> None:
        print("\n" + "=" * 40)
        print(" Project management")
        print("=" * 40)
        print("1. Create a new project")
        print("2. View all projects")
        print("3. Edit a project")
        print("4. Delete a project")
        print("5. Back to main menu")
        print("-" * 40)

    def display_tasks_menu(self) -> None:
        print("\n" + "=" * 40)
        print(" Task management")
        print("=" * 40)
        print("1. Create a new task")
        print("2. View tasks of a project")
        print("3. Edit a task")
        print("4. Change task status")
        print("5. Delete a task")
        print("6. Back to main menu")
        print("-" * 40)

    def run(self) -> None:
        print("Welcome to the ToDo List application!")
        while self.running:
            self.display_main_menu()
            choice = self.get_user_input("Your choice: ")

            if not self.running:
                break

            if choice == "1":
                self.handle_projects_menu()
            elif choice == "2":
                self.handle_tasks_menu()
            elif choice == "3":
                print("Thank you for using the system! Goodbye!")
                self.running = False
            else:
                print("Invalid choice. Please try again.")

    def handle_projects_menu(self) -> None:
        while self.running:
            self.display_projects_menu()
            choice = self.get_user_input("Your choice: ")

            if not self.running:
                break

            if choice == "1":
                self.create_project()
            elif choice == "2":
                self.list_projects()
            elif choice == "3":
                self.edit_project()
            elif choice == "4":
                self.delete_project()
            elif choice == "5":
                break
            else:
                print("Invalid choice. Please try again.")

    def create_project(self) -> None:
        print("\n--- Create a new project ---")
        name = self.get_user_input("Project name: ")
        if not self.running:
            return

        description = self.get_user_input("Project description: ")
        if not self.running:
            return

        try:
            project = self.project_service.create_project(
                name=name,
                description=description,
            )
            print(f"Project created successfully with ID: {project.id}")
        except Exception as exc:
            self.handle_error(exc)

    def list_projects(self) -> None:
        print("\n--- Project list ---")
        try:
            projects = self.project_service.list_projects()
            if not projects:
                print("No projects found.")
                return

            for project in projects:
                print("\n" + "-" * 40)
                print(f"ID: {project.id}")
                print(f"Name: {project.name}")
                print(f"Description: {project.description}")
                print(f"Created at: {project.created_at}")
            print("\nEnd of project list.")
        except Exception as exc:
            self.handle_error(exc)

    def edit_project(self) -> None:
        print("\n--- Edit a project ---")
        project_id = self.get_int_input("Project ID: ")
        if not self.running or project_id is None:
            return

        new_name = self.get_optional_input(
            "New name (leave empty to keep current): "
        )
        if not self.running:
            return

        new_description = self.get_optional_input(
            "New description (leave empty to keep current): "
        )
        if not self.running:
            return

        try:
            project = self.project_service.update_project(
                project_id=project_id,
                name=new_name,
                description=new_description,
            )
            print(f"Project with ID {project.id} updated successfully.")
        except Exception as exc:
            self.handle_error(exc)

    def delete_project(self) -> None:
        print("\n--- Delete a project ---")
        project_id = self.get_int_input("Project ID: ")
        if not self.running or project_id is None:
            return

        try:
            self.project_service.delete_project(project_id)
            print(f"Project with ID {project_id} deleted successfully.")
        except Exception as exc:
            self.handle_error(exc)

    def handle_tasks_menu(self) -> None:
        while self.running:
            self.display_tasks_menu()
            choice = self.get_user_input("Your choice: ")

            if not self.running:
                break

            if choice == "1":
                self.create_task()
            elif choice == "2":
                self.list_project_tasks()
            elif choice == "3":
                self.edit_task()
            elif choice == "4":
                self.change_task_status()
            elif choice == "5":
                self.delete_task()
            elif choice == "6":
                break
            else:
                print("Invalid choice. Please try again.")

    def create_task(self) -> None:
        print("\n--- Create a new task ---")
        project_id = self.get_int_input("Project ID: ")
        if not self.running or project_id is None:
            return

        title = self.get_user_input("Task title: ")
        if not self.running:
            return

        description = self.get_user_input("Task description: ")
        if not self.running:
            return

        status = self.get_optional_input(
            "Status (todo / doing / done) [default: todo]: "
        )
        if not self.running:
            return

        if not status:
            status = "todo"

        deadline = self.get_optional_input(
            "Deadline (YYYY-MM-DD) [optional]: "
        )
        if not self.running:
            return

        try:
            task = self.task_service.create_task(
                project_id=project_id,
                title=title,
                description=description,
                status=status,
                deadline=deadline,
            )
            print(f"Task created successfully with ID: {task.id}")
        except Exception as exc:
            self.handle_error(exc)

    def list_project_tasks(self) -> None:
        print("\n--- Tasks of a project ---")
        project_id = self.get_int_input("Project ID: ")
        if not self.running or project_id is None:
            return

        try:
            tasks = self.task_service.list_tasks_for_project(project_id)
            if not tasks:
                print("No tasks found for this project.")
                return

            status_icons = {
                "todo": "[ ]",
                "doing": "[~]",
                "done": "[x]",
            }

            for task in tasks:
                icon = status_icons.get(task.status, "[?]")
                print("\n" + "-" * 40)
                print(f"ID: {task.id}")
                print(f"Title: {task.title}")
                print(f"Description: {task.description}")
                print(f"{icon} Status: {task.status}")
                print(f"Deadline: {task.deadline or 'Not set'}")
                print(f"Created at: {task.created_at}")
                print(f"Closed at: {task.closed_at or 'Not closed'}")
            print("\nEnd of task list.")
        except Exception as exc:
            self.handle_error(exc)

    def edit_task(self) -> None:
        print("\n--- Edit a task ---")
        task_id = self.get_int_input("Task ID: ")
        if not self.running or task_id is None:
            return

        new_title = self.get_optional_input(
            "New title (leave empty to keep current): "
        )
        if not self.running:
            return

        new_description = self.get_optional_input(
            "New description (leave empty to keep current): "
        )
        if not self.running:
            return

        new_status = self.get_optional_input(
            "New status (todo / doing / done) [optional]: "
        )
        if not self.running:
            return

        new_deadline = self.get_optional_input(
            "New deadline (YYYY-MM-DD) [optional]: "
        )
        if not self.running:
            return

        try:
            task = self.task_service.update_task(
                task_id=task_id,
                title=new_title,
                description=new_description,
                status=new_status,
                deadline=new_deadline,
            )
            print(f"Task with ID {task.id} updated successfully.")
        except Exception as exc:
            self.handle_error(exc)

    def change_task_status(self) -> None:
        print("\n--- Change task status ---")
        task_id = self.get_int_input("Task ID: ")
        if not self.running or task_id is None:
            return

        new_status = self.get_user_input(
            "New status (todo / doing / done): "
        )
        if not self.running:
            return

        try:
            task = self.task_service.change_status(
                task_id=task_id,
                status=new_status,
            )
            print(
                f"Status of task with ID {task.id} "
                f"changed to '{task.status}'."
            )
        except Exception as exc:
            self.handle_error(exc)

    def delete_task(self) -> None:
        print("\n--- Delete a task ---")
        task_id = self.get_int_input("Task ID: ")
        if not self.running or task_id is None:
            return

        try:
            self.task_service.delete_task(task_id)
            print(f"Task with ID {task_id} deleted successfully.")
        except Exception as exc:
            self.handle_error(exc)
