from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from ...core.exceptions import NotFoundError, DuplicateError, ValidationError
from ..controller_schemas.requests import (
    ProjectCreateRequest,
    ProjectUpdateRequest,
)
from ..controller_schemas.responses import ProjectResponse
from ..dependencies import get_db_session, get_project_service
from ...services.project_service import ProjectService

router = APIRouter(prefix="/projects", tags=["projects"])


@router.post(
    "",
    response_model=ProjectResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_project(
    payload: ProjectCreateRequest,
    db: Session = Depends(get_db_session),
    project_service: ProjectService = Depends(get_project_service),
) -> ProjectResponse:
    project = project_service.create_project(
        name=payload.name,
        description=payload.description,
    )
    return ProjectResponse.model_validate(project)


@router.get(
    "",
    response_model=List[ProjectResponse],
    status_code=status.HTTP_200_OK,
)
def list_projects(
    db: Session = Depends(get_db_session),
    project_service: ProjectService = Depends(get_project_service),
) -> list[ProjectResponse]:
    projects = project_service.list_projects()
    return [ProjectResponse.model_validate(p) for p in projects]


@router.get(
    "/{project_id}",
    response_model=ProjectResponse,
    status_code=status.HTTP_200_OK,
)
def get_project(
    project_id: int,
    db: Session = Depends(get_db_session),
    project_service: ProjectService = Depends(get_project_service),
) -> ProjectResponse:
    project = project_service.get_project(project_id)
    return ProjectResponse.model_validate(project)


@router.patch(
    "/{project_id}",
    response_model=ProjectResponse,
    status_code=status.HTTP_200_OK,
)
def update_project(
    project_id: int,
    payload: ProjectUpdateRequest,
    db: Session = Depends(get_db_session),
    project_service: ProjectService = Depends(get_project_service),
) -> ProjectResponse:
    project = project_service.update_project(
        project_id=project_id,
        name=payload.name,
        description=payload.description,
    )
    return ProjectResponse.model_validate(project)


@router.delete(
    "/{project_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_project(
    project_id: int,
    db: Session = Depends(get_db_session),
    project_service: ProjectService = Depends(get_project_service),
) -> None:
    project_service.delete_project(project_id)
    return None
