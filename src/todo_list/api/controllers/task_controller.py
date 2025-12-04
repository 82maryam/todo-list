from typing import List

from fastapi import APIRouter, Depends, status

from ..controller_schemas.requests import (
    TaskCreateRequest,
    TaskUpdateRequest,
    TaskStatusChangeRequest,
)
from ..controller_schemas.responses import TaskResponse
from ..dependencies import get_db_session, get_task_service
from ...services.task_service import TaskService

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.post(
    "/projects/{project_id}",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_task_for_project(
    project_id: int,
    payload: TaskCreateRequest,
    task_service: TaskService = Depends(get_task_service),
) -> TaskResponse:
    task = task_service.create_task(
        project_id=project_id,
        title=payload.title,
        description=payload.description,
        status=payload.status or "todo",
        deadline=payload.deadline,
    )
    return TaskResponse.model_validate(task)


@router.get(
    "/projects/{project_id}",
    response_model=List[TaskResponse],
    status_code=status.HTTP_200_OK,
)
def list_tasks_for_project(
    project_id: int,
    task_service: TaskService = Depends(get_task_service),
) -> list[TaskResponse]:
    tasks = task_service.list_tasks_for_project(project_id)
    return [TaskResponse.model_validate(t) for t in tasks]


@router.get(
    "/{task_id}",
    response_model=TaskResponse,
    status_code=status.HTTP_200_OK,
)
def get_task(
    task_id: int,
    task_service: TaskService = Depends(get_task_service),
) -> TaskResponse:
    task = task_service.get_task(task_id)
    return TaskResponse.model_validate(task)


@router.patch(
    "/{task_id}",
    response_model=TaskResponse,
    status_code=status.HTTP_200_OK,
)
def update_task(
    task_id: int,
    payload: TaskUpdateRequest,
    task_service: TaskService = Depends(get_task_service),
) -> TaskResponse:
    task = task_service.update_task(
        task_id=task_id,
        title=payload.title,
        description=payload.description,
        status=payload.status,
        deadline=payload.deadline,
    )
    return TaskResponse.model_validate(task)


@router.patch(
    "/{task_id}/status",
    response_model=TaskResponse,
    status_code=status.HTTP_200_OK,
)
def change_task_status(
    task_id: int,
    payload: TaskStatusChangeRequest,
    task_service: TaskService = Depends(get_task_service),
) -> TaskResponse:
    task = task_service.change_status(
        task_id=task_id,
        status=payload.status,
    )
    return TaskResponse.model_validate(task)


@router.delete(
    "/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_task(
    task_id: int,
    task_service: TaskService = Depends(get_task_service),
) -> None:
    task_service.delete_task(task_id)
    return None
