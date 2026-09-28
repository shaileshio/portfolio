from datetime import UTC, datetime, timedelta

from uuid6 import uuid7

from app.core.config import get_settings
from app.core.security.hashing import get_hasher
from app.core.security.tokens.enum import TokenType
from app.core.security.tokens.provider import get_token_manager
from app.db.models import User
from app.db.repositories import UserRepository
from app.db.repositories.user_session import UserSessionRepository

from .errors import (
    ConfirmPasswordNotMatchError,
    EmailAlreadyExistError,
    InvalidPasswordError,
    UserNotFoundError,
)
from .schemas import LoginRequest, RegisterRequest, TokenResponse

settings = get_settings()


class AuthService:
    def __init__(
        self,
        user_repo: UserRepository,
        user_session_repo: UserSessionRepository,
    ) -> None:
        self._user_repo = user_repo
        self._user_session_repo = user_session_repo
        self._hasher = get_hasher()
        self.token_manager = get_token_manager()

    async def create_active_user(self, data: RegisterRequest) -> User:
        if data.password != data.confirm_password:
            raise ConfirmPasswordNotMatchError

        if await self._user_repo.email_exists(data.email):
            raise EmailAlreadyExistError

        user = await self._user_repo.create(
            data.email, self._hasher.hash(data.password)
        )

        await self._user_repo.session.commit()
        await self._user_repo.session.refresh(user)

        return user

    async def create_jwt_tokens(self, data: LoginRequest) -> TokenResponse:
        user = await self._user_repo.get_by_email(data.email)

        if user is None:
            raise UserNotFoundError

        if not self._hasher.verify(data.password, user.password_hash):
            raise InvalidPasswordError

        access = self.token_manager.create(
            subject=f"user:{user.id!s}",
            expire_minutes=settings.token.access_expire_minutes,
            claims={"type": TokenType.ACCESS.value},
        )
        refresh = self.token_manager.create(
            subject=f"user:{user.id!s}",
            expire_minutes=settings.token.refresh_expire_minutes,
            claims={"type": TokenType.REFRESH.value},
        )

        await self._user_session_repo.create(
            user_id=user.id,
            token_family_id=uuid7(),
            refresh_token_hash=self._hasher.hash(refresh),
            expires_at=datetime.now(UTC)
            + timedelta(minutes=settings.token.refresh_expire_minutes),
        )
        await self._user_session_repo.session.commit()

        return TokenResponse(access_token=access, refresh_token=refresh)
