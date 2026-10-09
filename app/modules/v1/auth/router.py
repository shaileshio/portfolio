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
    response_model=UserResponse,
)
async def get_me(request: Request, user: CurrentUserDep) -> User:
    return user
