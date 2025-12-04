from fastapi import APIRouter, FastAPI

from .controllers import project_router, task_router


def register_routers(app: FastAPI) -> None:
    api_router = APIRouter(prefix="/api")

    @api_router.get("/health", tags=["system"])
    async def health_check() -> dict:
        """Simple health check endpoint."""
        return {"status": "ok"}

    api_router.include_router(project_router)
    api_router.include_router(task_router)

    app.include_router(api_router)
