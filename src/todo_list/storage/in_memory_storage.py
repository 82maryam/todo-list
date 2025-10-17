from typing import Dict, List, Optional
import os

from ..core.entities import Project, Task
from ..core.exceptions import (
    DuplicateError,
    LimitExceededError,
    NotFoundError,
)


MAX_NUMBER_OF_PROJECTS = int(os.getenv("MAX_NUMBER_OF_PROJECTS", "100"))
MAX_NUMBER_OF_TASKS = int(os.getenv("MAX_NUMBER_OF_TASKS", "1000"))


class InMemoryStorage:
    
    def __init__(self) -> None:
        self._projects: Dict[int, Project] = {}
        self._tasks: Dict[int, Task] = {}
        self._project_counter: int = 0
        self._task_counter: int = 0
        self._project_names: set[str] = set()
    
    def _get_next_project_id(self) -> int:
        self._project_counter += 1
        return self._project_counter
    
    def _get_next_task_id(self) -> int:
        self._task_counter += 1
        return self._task_counter
    
    
    def create_project(self, name: str, description: str) -> Project:
     
        if len(self._projects) >= MAX_NUMBER_OF_PROJECTS:
            raise LimitExceededError(
                f"Project limit reached ({MAX_NUMBER_OF_PROJECTS})"
            )
        
        if name in self._project_names:
            raise DuplicateError(f"Project with name '{name}' already exists")
        
        project_id = self._get_next_project_id()
        project = Project(id=project_id, name=name, description=description)
        
        self._projects[project_id] = project
        self._project_names.add(name)
        
        return project
    
    def get_project(self, project_id: int) -> Project:
     
        if project_id not in self._projects:
            raise NotFoundError(f"Project with ID {project_id} not found")
        return self._projects[project_id]
    
    def update_project(
        self, project_id: int, name: Optional[str] = None, description: Optional[str] = None
    ) -> Project:
        
      
        project = self.get_project(project_id)
        
        old_name = project.name
        new_name = name if name is not None else old_name
        
        if new_name != old_name and new_name in self._project_names:
            raise DuplicateError(f"Project with name '{new_name}' already exists")
        
        project.update(name=name, description=description)
        
        if new_name != old_name:
            self._project_names.remove(old_name)
            self._project_names.add(new_name)
        
        return project
    
    def delete_project(self, project_id: int) -> None:
        
        project = self.get_project(project_id)
        
        for task_id in list(project.tasks.keys()):
            del self._tasks[task_id]
            project.remove_task(task_id)
        
        self._project_names.remove(project.name)
        del self._projects[project_id]
    
    def get_all_projects(self) -> List[Project]:
      
        return sorted(
            self._projects.values(),
            key=lambda p: p.created_at
        )
    
    
    def create_task(
        self,
        project_id: int,
        title: str,
        description: str,
        status: str = "todo",
        deadline: Optional[str] = None,
    ) -> Task:
        
      
        if len(self._tasks) >= MAX_NUMBER_OF_TASKS:
            raise LimitExceededError(
                f"Task limit reached ({MAX_NUMBER_OF_TASKS})"
            )
        
        project = self.get_project(project_id)
        
        task_id = self._get_next_task_id()
        task = Task(
            id=task_id,
            title=title,
            description=description,
            status=status,
            deadline=deadline,
        )
        
        self._tasks[task_id] = task
        project.add_task(task)
        
        return task
    
    def get_task(self, task_id: int) -> Task:
 
        if task_id not in self._tasks:
            raise NotFoundError(f"Task with ID {task_id} not found")
        return self._tasks[task_id]
    
    def update_task(
        self,
        task_id: int,
        title: Optional[str] = None,
        description: Optional[str] = None,
        status: Optional[str] = None,
        deadline: Optional[str] = None,
    ) -> Task:
  
        task = self.get_task(task_id)
        task.update(
            title=title,
            description=description,
            status=status,
            deadline=deadline,
        )
        return task
    
    def delete_task(self, task_id: int) -> None:
    
        task = self.get_task(task_id)
        
        for project in self._projects.values():
            if task_id in project.tasks:
                project.remove_task(task_id)
                break
        
        del self._tasks[task_id]
    
    def get_project_tasks(self, project_id: int) -> List[Task]:
        
        project = self.get_project(project_id)
        return sorted(
            project.tasks.values(),
            key=lambda t: t.created_at
        )
    
    def change_task_status(self, task_id: int, status: str) -> Task:
       
        return self.update_task(task_id, status=status)