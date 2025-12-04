from fastapi import APIRouter, FastAPI


def register_routers(app: FastAPI) -> None:
    api_router = APIRouter(prefix="/api")

    @api_router.get("/health", tags=["system"])
    async def health_check() -> dict:
        return {"status": "ok"}

    app.include_router(api_router)
