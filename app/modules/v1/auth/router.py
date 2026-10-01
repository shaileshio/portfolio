from fastapi import APIRouter, Request

from app.db.depends import AsyncSessionDep
from app.db.models.user import User

from .depends import AuthServiceDep
from .schemas import (
    LoginRequest,
    LogoutRequest,
    RefreshRequest,
    RegisterRequest,
    RegisterResponse,
    TokenResponse,
)

router = APIRouter(prefix="/auth", tags=["Authencation"])


@router.post(
    "/register",
    summary="Create a new user account",
    description="Register a new user account for authentication.",
    response_model=RegisterResponse,
)
async def register(data: RegisterRequest, service: AuthServiceDep) -> User:
    return await service.create_active_user(data)


@router.post(
    "/login",
    summary="Issue new jwt tokens",
    description="Issue new jwt tokens to make requests on protected routes.",
)
async def login(
    request: Request, data: LoginRequest, service: AuthServiceDep
) -> TokenResponse:
    return await service.create_jwt_tokens(request, data)


@router.post(
    "/refresh",
    summary="Refresh access token",
    description="Issue a new access token using a valid refresh token.",
)
async def refresh(
    request: Request, data: RefreshRequest, service: AuthServiceDep
) -> TokenResponse:
    return await service.rotate_refresh_token(request, data.refresh_token)


@router.post(
    "/logout",
    summary="Log out of the current session",
    description="Log out by invalidating the current authentication session.",
)
async def logout(data: LogoutRequest, session: AsyncSessionDep): ...
