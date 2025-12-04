from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from ..core.exceptions import (
    ValidationError as DomainValidationError,
    DuplicateError,
    LimitExceededError,
    NotFoundError,
    TodoListError,
)
from .routers import register_routers


def create_app() -> FastAPI:
    app = FastAPI(
        title="ToDo List API",
        version="1.0.0",
        description="Web API for managing projects and tasks.",
    )

    register_routers(app)
    register_exception_handlers(app)

    return app


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(DomainValidationError)
    async def validation_error_handler(
        request: Request, exc: DomainValidationError
    ) -> JSONResponse:
        return JSONResponse(
            status_code=400,
            content={"detail": str(exc)},
        )

    @app.exception_handler(DuplicateError)
    async def duplicate_error_handler(
        request: Request, exc: DuplicateError
    ) -> JSONResponse:
        return JSONResponse(
            status_code=409,
            content={"detail": str(exc)},
        )

    @app.exception_handler(LimitExceededError)
    async def limit_exceeded_handler(
        request: Request, exc: LimitExceededError
    ) -> JSONResponse:
        return JSONResponse(
            status_code=400,
            content={"detail": str(exc)},
        )

    @app.exception_handler(NotFoundError)
    async def not_found_handler(
        request: Request, exc: NotFoundError
    ) -> JSONResponse:
        return JSONResponse(
            status_code=404,
            content={"detail": str(exc)},
        )

    @app.exception_handler(TodoListError)
    async def generic_todolist_error_handler(
        request: Request, exc: TodoListError
    ) -> JSONResponse:
        return JSONResponse(
            status_code=500,
            content={"detail": str(exc)},
        )


# Uvicorn entrypoint: `todo_list.api.main:app`
app = create_app()
