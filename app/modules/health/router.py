from fastapi import APIRouter, HTTPException
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from app.db.depends import AsyncSessionDep

from .schemas import HealthReadyErrorResponse, HealthReadyResponse, HealthResponse

router = APIRouter(prefix="/health", tags=["Health"])


@router.get(
    "/",
    summary="Check API health",
    description="Returns the current health status of the API.",
)
async def health() -> HealthResponse:
    return HealthResponse(status="ok")


@router.get(
    "/ready",
    summary="Check API readiness",
    description="Checks whether the API and its database are ready to serve requests.",
    responses={503: {"model": HealthReadyErrorResponse}},
)
async def ready(session: AsyncSessionDep) -> HealthReadyResponse:
    try:
        await session.execute(text("SELECT 1"))

        return HealthReadyResponse(status="ok", database="connected")
    except SQLAlchemyError:
        raise HTTPException(
            status_code=503,
            detail={
                "status": "error",
                "database": "disconnected",
            },
        )
