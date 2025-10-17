from ..storage.in_memory_storage import InMemoryStorage
from ..core.exceptions import (
    TodoListError,
    ValidationError,
    DuplicateError,
    LimitExceededError,
    NotFoundError,
)


class CLIInterface:

    def __init__(self) -> None:
        self.storage = InMemoryStorage()
        self.running = True

    def display_menu(self) -> None:
        print("\n" + "=" * 50)
        print(" ToDoList Management System")
        print("=" * 50)
        print("1. Manage Projects")
        print("2. Manage Tasks")
        print("3. Exit")
        print("-" * 50)

    def display_projects_menu(self) -> None:
        print("\n" + "=" * 30)
        print(" Project Management")
        print("=" * 30)
        print("1. Create a new project")
        print("2. View all projects")
        print("3. Edit a project")
        print("4. Delete a project")
        print("5. Back to main menu")
        print("-" * 30)

    def display_tasks_menu(self) -> None:
        print("\n" + "=" * 30)
        print(" Task Management")
        print("=" * 30)
        print("1. Create a new task")
        print("2. View tasks of a project")
        print("3. Edit a task")
        print("4. Change task status")
        print("5. Delete a task")
        print("6. Back to main menu")
        print("-" * 30)

    def get_user_input(self, prompt: str, required: bool = True) -> str:
     
        while True:
            try:
                user_input = input(prompt).strip()
                if required and not user_input:
                    print(" This field is required. Please enter a value.")
                    continue
                return user_input
            except KeyboardInterrupt:
                print("\n\n Exiting program...")
                self.running = False
                return ""
            except EOFError:
                print("\n\n Exiting program...")
                self.running = False
                return ""

    def handle_error(self, error: Exception) -> None:
        if isinstance(error, ValidationError):
            print(f" Validation Error: {error}")
        elif isinstance(error, DuplicateError):
            print(f" Duplicate Error: {error}")
        elif isinstance(error, LimitExceededError):
            print(f" Limit Exceeded: {error}")
        elif isinstance(error, NotFoundError):
            print(f" Not Found: {error}")
        elif isinstance(error, TodoListError):
            print(f" System Error: {error}")
        else:
            print(f" Unknown Error: {error}")

    def show_success_message(self, message: str) -> None:
        print(f" {message}")


    def create_project(self) -> None:
        print("\n--- Create New Project ---")

        name = self.get_user_input("Project name: ")
        description = self.get_user_input("Project description: ", required=False)

        try:
            project = self.storage.create_project(name, description)
            self.show_success_message(
                f"Project '{project.name}' created with ID {project.id}"
            )
        except TodoListError as e:
            self.handle_error(e)

    def list_projects(self) -> None:
        print("\n--- Project List ---")
        
        try:
            projects = self.storage.get_all_projects()
            if not projects:
                print(" No projects found")
                return
            
            for project in projects:
                print(f"\n ID: {project.id}")
                print(f" Name: {project.name}")
                print(f" Description: {project.description}")
                print(f" Task Count: {project.task_count}") 
                print(f" Created At: {project.created_at}")
                print("-" * 30)
                
        except TodoListError as e:
            self.handle_error(e)

    def update_project(self) -> None:
        print("\n--- Edit Project ---")

        try:
            project_id = int(self.get_user_input("Project ID: "))
            project = self.storage.get_project(project_id)

            print(f"\nCurrent Project:")
            print(f"Name: {project.name}")
            print(f"Description: {project.description}")

            new_name = (
                self.get_user_input(f"New name (current: {project.name}): ", required=False)
                or project.name
            )
            new_description = (
                self.get_user_input(
                    f"New description (current: {project.description}): ", required=False
                )
                or project.description
            )

            updated_project = self.storage.update_project(
                project_id, new_name, new_description
            )
            self.show_success_message(f"Project '{updated_project.name}' updated successfully.")

        except ValueError:
            print(" Project ID must be a number.")
        except TodoListError as e:
            self.handle_error(e)

    def delete_project(self) -> None:
        print("\n--- Delete Project ---")

        try:
            project_id = int(self.get_user_input("Project ID: "))
            project = self.storage.get_project(project_id)

            confirm = self.get_user_input(
                f"Are you sure you want to delete project '{project.name}' and all its tasks? (y/n): "
            ).lower()

            if confirm == "y":
                self.storage.delete_project(project_id)
                self.show_success_message(f"Project '{project.name}' deleted successfully.")
            else:
                print(" Deletion cancelled.")

        except ValueError:
            print("Project ID must be a number.")
        except TodoListError as e:
            self.handle_error(e)


    def create_task(self) -> None:
        """Create a new task."""
        print("\n--- Create New Task ---")

        try:
            project_id = int(self.get_user_input("Project ID: "))
            self.storage.get_project(project_id)

            title = self.get_user_input("Task title: ")
            description = self.get_user_input("Task description: ", required=False)

            print("Task status:")
            print("1. todo (default)")
            print("2. doing")
            print("3. done")

            status_choice = self.get_user_input("Choose status (1-3) [default: 1]: ", required=False)
            status_map = {"1": "todo", "2": "doing", "3": "done"}
            status = status_map.get(status_choice, "todo")

            deadline = self.get_user_input("Deadline (YYYY-MM-DD) [optional]: ", required=False) or None

            task = self.storage.create_task(project_id, title, description, status, deadline)
            self.show_success_message(f"Task '{task.title}' created with ID {task.id}")

        except ValueError:
            print(" Project ID must be a number.")
        except TodoListError as e:
            self.handle_error(e)

    def list_project_tasks(self) -> None:
        print("\n--- Project Tasks ---")

        try:
            project_id = int(self.get_user_input("Project ID: "))
            project = self.storage.get_project(project_id)
            tasks = self.storage.get_project_tasks(project_id)

            print(f"\n Project: {project.name}")
            print(f" Description: {project.description}")
            print(f" Number of tasks: {len(tasks)}")
            print("=" * 40)

            if not tasks:
                print(" No tasks in this project.")
                return

            for task in tasks:
                status_icons = {"todo", "doing", "done"}
                icon = status_icons.get(task.status, )

                print(f"\n ID: {task.id}")
                print(f"Title: {task.title}")
                print(f" Description: {task.description}")
                print(f"{icon} Status: {task.status}")
                print(f" Deadline: {task.deadline or 'Not set'}")
                print(f" Created At: {task.created_at}")
                print("-" * 30)

        except ValueError:
            print(" Project ID must be a number.")
        except TodoListError as e:
            self.handle_error(e)

    def update_task(self) -> None:
        print("\n--- Edit Task ---")

        try:
            task_id = int(self.get_user_input("Task ID: "))
            task = self.storage.get_task(task_id)

            print(f"\nCurrent Task:")
            print(f"Title: {task.title}")
            print(f"Description: {task.description}")
            print(f"Status: {task.status}")
            print(f"Deadline: {task.deadline or 'Not set'}")

            new_title = (
                self.get_user_input(f"New title (current: {task.title}): ", required=False)
                or task.title
            )
            new_description = (
                self.get_user_input(f"New description (current: {task.description}): ", required=False)
                or task.description
            )

            print("New status:")
            print("1. todo")
            print("2. doing")
            print("3. done")

            status_choice = self.get_user_input(
                f"Choose new status (current: {task.status}) [1-3]: ", required=False
            )
            status_map = {"1": "todo", "2": "doing", "3": "done"}
            new_status = status_map.get(status_choice, task.status)

            new_deadline = (
                self.get_user_input(
                    f"New deadline (current: {task.deadline or 'Not set'}): ",
                    required=False,
                )
                or task.deadline
            )

            if new_deadline == "Not set":
                new_deadline = None

            updated_task = self.storage.update_task(
                task_id, new_title, new_description, new_status, new_deadline
            )
            self.show_success_message(f"Task '{updated_task.title}' updated successfully.")

        except ValueError:
            print(" Task ID must be a number.")
        except TodoListError as e:
            self.handle_error(e)

    def change_task_status(self) -> None:
        print("\n--- Change Task Status ---")

        try:
            task_id = int(self.get_user_input("Task ID: "))
            task = self.storage.get_task(task_id)

            print(f"\nCurrent Task: {task.title}")
            print(f"Current Status: {task.status}")

            print("\nNew status:")
            print("1. todo")
            print("2. doing")
            print("3. done")

            status_choice = self.get_user_input("Choose new status (1-3): ")
            status_map = {"1": "todo", "2": "doing", "3": "done"}

            if status_choice not in status_map:
                print(" Invalid choice.")
                return

            new_status = status_map[status_choice]
            updated_task = self.storage.change_task_status(task_id, new_status)
            self.show_success_message(
                f"Task '{updated_task.title}' status changed to '{new_status}'."
            )

        except ValueError:
            print(" Task ID must be a number.")
        except TodoListError as e:
            self.handle_error(e)

    def delete_task(self) -> None:
        """Delete a task."""
        print("\n--- Delete Task ---")

        try:
            task_id = int(self.get_user_input("Task ID: "))
            task = self.storage.get_task(task_id)

            confirm = self.get_user_input(
                f"Are you sure you want to delete task '{task.title}'? (y/n): "
            ).lower()

            if confirm == "y":
                self.storage.delete_task(task_id)
                self.show_success_message(f"Task '{task.title}' deleted successfully.")
            else:
                print(" Deletion cancelled.")

        except ValueError:
            print(" Task ID must be a number.")
        except TodoListError as e:
            self.handle_error(e)


    def handle_projects_menu(self) -> None:
        while self.running:
            self.display_projects_menu()
            choice = self.get_user_input("Your choice: ")

            if choice == "1":
                self.create_project()
            elif choice == "2":
                self.list_projects()
            elif choice == "3":
                self.update_project()
            elif choice == "4":
                self.delete_project()
            elif choice == "5":
                break
            else:
                print(" Invalid choice.")

    def handle_tasks_menu(self) -> None:
        while self.running:
            self.display_tasks_menu()
            choice = self.get_user_input("Your choice: ")

            if choice == "1":
                self.create_task()
            elif choice == "2":
                self.list_project_tasks()
            elif choice == "3":
                self.update_task()
            elif choice == "4":
                self.change_task_status()
            elif choice == "5":
                self.delete_task()
            elif choice == "6":
                break
            else:
                print(" Invalid choice.")

    def run(self) -> None:
        print(" Welcome to the ToDoList Management System!")

        while self.running:
            self.display_menu()
            choice = self.get_user_input("Your choice: ")

            if choice == "1":
                self.handle_projects_menu()
            elif choice == "2":
                self.handle_tasks_menu()
            elif choice == "3":
                print(" Thank you for using the system! Goodbye!")
                self.running = False
            else:
                print(" Invalid choice.")
