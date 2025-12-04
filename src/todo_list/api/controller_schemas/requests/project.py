from pydantic import BaseModel, Field


class ProjectCreateRequest(BaseModel):
    name: str = Field(..., description="Project name")
    description: str = Field(..., description="Project description")


class ProjectUpdateRequest(BaseModel):
    name: str | None = Field(
        default=None,
        description="New project name (optional)",
    )
    description: str | None = Field(
        default=None,
        description="New project description (optional)",
    )
