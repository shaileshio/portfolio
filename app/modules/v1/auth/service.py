from datetime import timedelta

from fastapi import Request
from sqlalchemy.ext.asyncio import AsyncSession
from uuid6 import uuid7

from app.core.config import get_settings
from app.core.security.hashing import get_hasher
from app.core.security.tokens.enum import TokenType
from app.core.security.tokens.provider import get_token_manager
from app.db.models import User
from app.db.repositories import UserRepository
from app.db.repositories.user_session import UserSessionRepository
from app.shared.datetime import get_utc_now
from app.shared.request import (
    get_device_name,
    get_ip_address,
    get_user_agent,
)

from .errors import (
    ConfirmPasswordNotMatchError,
    EmailAlreadyExistError,
    InvalidPasswordError,
    UserNotFoundError,
)
from .schemas import LoginRequest, RegisterRequest, TokenResponse

settings = get_settings()

access_token_lifetime = settings.auth.access_token_lifetime
refresh_token_lifetime = settings.auth.refresh_token_lifetime
session_lifetime = settings.auth.session_lifetime


class AuthService:
    def __init__(
        self,
        session: AsyncSession,
        user_repo: UserRepository,
        user_session_repo: UserSessionRepository,
    ) -> None:
        self._session = session
        self._user_repo = user_repo
        self._user_session_repo = user_session_repo
        self._hasher = get_hasher()
        self._token_manager = get_token_manager()

    async def create_active_user(self, data: RegisterRequest) -> User:
        if data.password != data.confirm_password:
            raise ConfirmPasswordNotMatchError

        if await self._user_repo.email_exists(data.email):
            raise EmailAlreadyExistError

        user = await self._user_repo.create(
            data.email, self._hasher.hash(data.password)
        )

        await self._session.commit()
        await self._session.refresh(user)

        return user

    async def create_jwt_tokens(
        self, request: Request, data: LoginRequest
    ) -> TokenResponse:
        user = await self._user_repo.get_by_email(data.email)

        if user is None:
            raise UserNotFoundError

        if not self._hasher.verify(data.password, user.password_hash):
            raise InvalidPasswordError

        utc_now = get_utc_now()
        subject = str(user.id)

        access_expires_at = utc_now + timedelta(minutes=access_token_lifetime)
        refresh_expires_at = utc_now + timedelta(minutes=refresh_token_lifetime)

        session = await self._user_session_repo.create(
            user_id=user.id,
            refresh_token_hash=str(uuid7()),
            refresh_expires_at=refresh_expires_at,
            session_expires_at=utc_now + timedelta(minutes=session_lifetime),
            ip_address=get_ip_address(request),
            user_agent=get_user_agent(request),
            device_name=get_device_name(request),
        )

        access_token = self._token_manager.create(
            subject=subject,
            expires_at=access_expires_at,
            claims={"type": TokenType.ACCESS.value},
        )
        refresh_token = self._token_manager.create(
            subject=subject,
            expires_at=refresh_expires_at,
            claims={"type": TokenType.REFRESH.value, "sid": str(session.id)},
        )

        session.refresh_token_hash = self._hasher.hash(refresh_token)
        await self._session.commit()

        return TokenResponse(access_token=access_token, refresh_token=refresh_token)
