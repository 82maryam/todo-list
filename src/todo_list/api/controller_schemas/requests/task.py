from pydantic import BaseModel, Field


class TaskCreateRequest(BaseModel):
    title: str = Field(..., description="Task title")
    description: str = Field(..., description="Task description")
    status: str | None = Field(
        default="todo",
        description="Task status (todo / doing / done)",
    )
    deadline: str | None = Field(
        default=None,
        description="Deadline in YYYY-MM-DD format (optional)",
    )


class TaskUpdateRequest(BaseModel):
    title: str | None = Field(
        default=None,
        description="New title (optional)",
    )
    description: str | None = Field(
        default=None,
        description="New description (optional)",
    )
    status: str | None = Field(
        default=None,
        description="New status (todo / doing / done) (optional)",
    )
    deadline: str | None = Field(
        default=None,
        description="New deadline in YYYY-MM-DD (optional)",
    )


class TaskStatusChangeRequest(BaseModel):
    status: str = Field(
        ...,
        description="New status (todo / doing / done)",
    )
