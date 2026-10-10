from datetime import datetime
from ipaddress import IPv4Address, IPv6Address
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..models import UserSession

type IPAddress = IPv4Address | IPv6Address


class UserSessionRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(
        self,
        *,
        user_id: UUID,
        refresh_token_hash: str,
        refresh_expires_at: datetime,
        session_expires_at: datetime,
        ip_address: IPAddress | None,
        user_agent: str | None,
        device_name: str | None,
    ) -> UserSession:
        session = UserSession(
            user_id=user_id,
            refresh_token_hash=refresh_token_hash,
            refresh_expires_at=refresh_expires_at,
            session_expires_at=session_expires_at,
            ip_address=ip_address,
            user_agent=user_agent,
            device_name=device_name,
        )

        self._session.add(session)
        await self._session.flush()

        return session

    async def get_by_session_id(self, session_id: UUID) -> UserSession | None:
        stmt = select(UserSession).where(
            UserSession.id == session_id,
        )

        result = await self._session.execute(stmt)

        return result.scalar_one_or_none()

    async def get_by_user_id(self, user_id: UUID) -> UserSession | None:
        stmt = select(UserSession).where(
            UserSession.user_id == user_id,
        )

        result = await self._session.execute(stmt)

        return result.scalar_one_or_none()

    async def get_by_ids(self, user_id: UUID, session_id: UUID) -> UserSession | None:
        stmt = select(UserSession).where(
            UserSession.user_id == user_id,
            UserSession.id == session_id,
        )

        result = await self._session.execute(stmt)

        return result.scalar_one_or_none()

    async def list_active_session(
        self, user_id: UUID, session_id: UUID
    ) -> list[UserSession]:
        stmt = select(UserSession).where(
            UserSession.user_id == user_id,
            UserSession.id == session_id,
        )

        sesstions = (await self._session.scalars(stmt)).all()

        return list(filter(lambda session: session.is_active(), sesstions))
