from typing import cast
from uuid import UUID

from fastapi import APIRouter, Request

from app.db.models.user import User
from app.shared.depends import CurrentUserDep
from app.shared.schemas import DetailResponse

from .depends import AuthServiceDep
from .schemas import (
    TokenRefresh,
    TokenResponse,
    UserLogin,
    UserLogout,
    UserRegister,
    UserResponse,
    UserSessionListResponse,
    UserSessionResponse,
)

router = APIRouter(prefix="/auth", tags=["Authencation"])


@router.post(
    "/register",
    summary="Create a new user account",
    description="Register a new user account for authentication.",
    response_model=UserResponse,
)
async def register(data: UserRegister, service: AuthServiceDep) -> User:
    return await service.create_active_user(
        data.email, data.password, data.confirm_password
    )


@router.post(
    "/login",
    summary="Issue new jwt tokens",
    description="Issue new jwt tokens to make requests on protected routes.",
)
async def login(
    request: Request, data: UserLogin, service: AuthServiceDep
) -> TokenResponse:
    return await service.create_jwt_tokens(request, data.email, data.password)


@router.post(
    "/refresh",
    summary="Refresh access token",
    description="Issue a new access token using a valid refresh token.",
)
async def refresh(
    request: Request, data: TokenRefresh, service: AuthServiceDep
) -> TokenResponse:
    return await service.rotate_refresh_token(request, data.refresh_token)


@router.post(
    "/logout",
    summary="Log out of the current session",
    description="Log out by invalidating the current authentication session.",
)
async def logout(
    request: Request, data: UserLogout, service: AuthServiceDep
) -> DetailResponse:
    return await service.logout(request, data.refresh_token)


@router.get(
    "/me",
    summary="Get current authenticated user",
    description="Return the authenticated user's profile information for the current session.",
)
async def get_me(request: Request, user: CurrentUserDep) -> UserResponse:
    return cast(UserResponse, user)


@router.get(
    "/sessions",
    summary="List active user sessions",
    description="Retrieve all active authentication sessions for the current user.",
)
async def list_sessions(
    user: CurrentUserDep, service: AuthServiceDep
) -> UserSessionListResponse:
    sessions = await service.list_active_sessions(user.id)

    return UserSessionListResponse(
        sessions=cast(list[UserSessionResponse], sessions),
    )


@router.get(
    "/sessions/{session_id}",
    summary="get active user session",
    description="Retrieve a single active authentication session for the current user.",
)
async def get_session(
    user: CurrentUserDep, session_id: UUID, service: AuthServiceDep
) -> UserSessionResponse:
    session = await service.get_active_session(user.id, session_id)

    return cast(UserSessionResponse, session)
