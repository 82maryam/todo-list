from datetime import datetime, date
from typing import Optional

from pydantic import BaseModel, ConfigDict


class TaskResponse(BaseModel):
    id: int
    title: str
    description: str
    status: str
    deadline: Optional[date]
    created_at: datetime
    closed_at: Optional[datetime]
    project_id: int

    model_config = ConfigDict(from_attributes=True)
