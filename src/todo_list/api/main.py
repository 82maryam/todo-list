from fastapi import FastAPI

from .routers import register_routers


def create_app() -> FastAPI:
    app = FastAPI(
        title="ToDo List API",
        version="1.0.0",
        description="Web API for managing projects and tasks.",
    )

    register_routers(app)
    return app


app = create_app()
