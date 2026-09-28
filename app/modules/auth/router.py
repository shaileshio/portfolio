from fastapi import APIRouter

from app.db.depends import AsyncSessionDep
from app.db.models.user import User
from app.modules.auth.schemas import TokenResponse

from .depends import AuthServiceDep
from .schemas import LoginRequest, LogoutRequest, RegisterRequest, RegisterResponse

router = APIRouter(prefix="/auth", tags=["Authencation"])


@router.post("/register", response_model=RegisterResponse)
async def register(data: RegisterRequest, service: AuthServiceDep) -> User:
    return await service.create_active_user(data)


@router.post(
    "/login",
    summary="Issue new jwt tokens",
    description="Issue new jwt tokens to make requests on protected routes.",
)
async def login(data: LoginRequest, service: AuthServiceDep) -> TokenResponse:
    return await service.create_jwt_tokens(data)


@router.post("/logout")
async def logout(data: LogoutRequest, session: AsyncSessionDep): ...
