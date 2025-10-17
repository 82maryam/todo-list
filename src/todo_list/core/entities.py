from datetime import datetime
from typing import Optional
from dataclasses import dataclass, field
from .validators import Validator


@dataclass
class Task:
    
    id: int
    title: str
    description: str
    status: str = "todo"
    deadline: Optional[str] = None
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    
    def __post_init__(self) -> None:
        self.title = Validator.validate_text(self.title, "task", 30)
        self.description = Validator.validate_text(
            self.description, "dicripition", 150, allow_empty=True
        )
        self.status = Validator.validate_status(self.status)
        self.deadline = Validator.validate_deadline(self.deadline)
    
    def update(
        self,
        title: Optional[str] = None,
        description: Optional[str] = None,
        status: Optional[str] = None,
        deadline: Optional[str] = None,
    ) -> None:
        if title is not None:
            self.title = Validator.validate_text(title, "update", 30)
        if description is not None:
            self.description = Validator.validate_text(
                description, "discription", 150, allow_empty=True
            )
        if status is not None:
            self.status = Validator.validate_status(status)
        if deadline is not None:
            self.deadline = Validator.validate_deadline(deadline)
    
    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "status": self.status,
            "deadline": self.deadline,
            "created_at": self.created_at,
        }


@dataclass
class Project:
    
    id: int
    name: str
    description: str
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    tasks: dict[int, Task] = field(default_factory=dict)
    
    def __post_init__(self) -> None:
        self.name = Validator.validate_text(self.name, "project name", 30)
        self.description = Validator.validate_text(
            self.description, "discription project", 150, allow_empty=True
        )
    
    @property
    def task_count(self) -> int:
        return len(self.tasks)
    
    def update(self, name: Optional[str] = None, description: Optional[str] = None) -> None:
        if name is not None:
            self.name = Validator.validate_text(name, "project name", 30)
        if description is not None:
            self.description = Validator.validate_text(
                description, "discription project", 150, allow_empty=True
            )
    
    def add_task(self, task: Task) -> None:
        self.tasks[task.id] = task
    
    def remove_task(self, task_id: int) -> None:
        if task_id not in self.tasks:
            raise KeyError(f"id task{task_id} not excist")
        del self.tasks[task_id]
    
    def get_task(self, task_id: int) -> Task:
        if task_id not in self.tasks:
            raise KeyError(f"id task{task_id}not excist")
        return self.tasks[task_id]
    
    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "created_at": self.created_at,
            "task_count": self.task_count,
        }