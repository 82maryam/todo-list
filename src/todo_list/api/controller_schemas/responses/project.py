from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ProjectResponse(BaseModel):
    id: int
    name: str
    description: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
