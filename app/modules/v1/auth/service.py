from datetime import timedelta
from uuid import UUID

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
from app.shared.schemas import DetailResponse

from .errors import (
    ConfirmPasswordNotMatchError,
    EmailAlreadyExistError,
    InvalidPasswordError,
    InvalidTokenError,
    SessionExpiredError,
    TokenRevokedError,
    UserNotFoundError,
)
from .schemas import TokenResponse

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

    async def create_active_user(
        self, email: str, password: str, confirm_password: str
    ) -> User:

        if password != confirm_password:
            raise ConfirmPasswordNotMatchError

        if await self._user_repo.email_exists(email):
            raise EmailAlreadyExistError

        user = await self._user_repo.create(email, self._hasher.hash(password))

        await self._session.commit()
        await self._session.refresh(user)

        return user

    async def create_jwt_tokens(
        self, request: Request, email: str, password: str
    ) -> TokenResponse:
        user = await self._user_repo.get_by_email(email)

        if user is None:
            raise UserNotFoundError

        if not self._hasher.verify(password, user.password_hash):
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
            issue_at=utc_now,
            expires_at=access_expires_at,
            claims={
                "type": TokenType.ACCESS.value,
                "sid": str(session.id),
            },
        )
        refresh_token = self._token_manager.create(
            subject=subject,
            issue_at=utc_now,
            expires_at=refresh_expires_at,
            claims={
                "type": TokenType.REFRESH.value,
                "sid": str(session.id),
            },
        )

        session.refresh_token_hash = self._hasher.hash(refresh_token)

        await self._session.commit()

        return TokenResponse(access_token=access_token, refresh_token=refresh_token)

    async def rotate_refresh_token(
        self, request: Request, refresh_token: str
    ) -> TokenResponse:

        claims = self._token_manager.verify(refresh_token)

        try:
            user_id = claims["sub"]
            session_id = claims["sid"]
        except KeyError:
            raise InvalidTokenError

        session = await self._user_session_repo.get_by_ids(
            user_id=UUID(user_id), session_id=UUID(session_id)
        )

        if (
            claims["type"] != TokenType.REFRESH.value
            or not session
            or not self._hasher.verify(
                value=refresh_token,
                hashed=session.refresh_token_hash,
            )
        ):
            raise InvalidTokenError

        if session.is_revoked:
            raise TokenRevokedError

        if session.is_session_expired():
            raise SessionExpiredError

        utc_now = get_utc_now()

        refresh_expires_at = utc_now + timedelta(minutes=refresh_token_lifetime)
        access_expires_at = utc_now + timedelta(minutes=access_token_lifetime)

        if session.is_refresh_expired():
            refresh_token = self._token_manager.create(
                subject=claims["sub"],
                issue_at=utc_now,
                expires_at=refresh_expires_at,
                claims={
                    "type": TokenType.REFRESH.value,
                    "sid": str(session.id),
                },
            )

            session.refresh_token_hash = self._hasher.hash(refresh_token)
            session.refresh_expires_at = refresh_expires_at

        access_token = self._token_manager.create(
            subject=claims["sub"],
            issue_at=utc_now,
            expires_at=access_expires_at,
            claims={
                "type": TokenType.ACCESS.value,
                "sid": str(session.id),
            },
        )

        session.touch()

        session.ip_address = get_ip_address(request)
        session.user_agent = get_user_agent(request)
        session.device_name = get_device_name(request)

        await self._session.commit()

        return TokenResponse(access_token=access_token, refresh_token=refresh_token)

    async def logout(self, request: Request, refresh_token: str) -> DetailResponse:

        claims = self._token_manager.verify(refresh_token)

        try:
            user_id = claims["sub"]
            session_id = claims["sid"]
        except KeyError:
            raise InvalidTokenError

        session = await self._user_session_repo.get_by_ids(
            user_id=UUID(user_id), session_id=UUID(session_id)
        )

        if (
            claims["type"] != TokenType.REFRESH.value
            or not session
            or not self._hasher.verify(
                value=refresh_token,
                hashed=session.refresh_token_hash,
            )
        ):
            raise InvalidTokenError

        if not session.is_revoked:
            session.touch()
            session.revoke()

            session.ip_address = get_ip_address(request)
            session.user_agent = get_user_agent(request)
            session.device_name = get_device_name(request)

            await self._session.commit()

        return DetailResponse(detail="Logout successful")
