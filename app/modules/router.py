from fastapi import APIRouter

from app.core.config import get_settings
from app.shared.schemas import DetailResponse

from .health.router import router as health_router
from .v1.router import router as v1_router

settings = get_settings()

title = settings.app.title

router = APIRouter()


@router.get(
    "/",
    summary="Welcome",
    description=f"Welcome endpoint for the {title} API.",
)
async def welcome() -> DetailResponse:
    return DetailResponse(detail="Hello! How can I help you?")


router.include_router(health_router)
router.include_router(v1_router, prefix="/api/v1")
