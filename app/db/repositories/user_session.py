from datetime import datetime
from ipaddress import IPv4Address, IPv6Address
from uuid import UUID

from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from ..models import UserSession

IPAddress = IPv4Address | IPv6Address


class UserSessionRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(
        self,
        *,
        user_id: UUID,
        token_family_id: UUID,
        refresh_token_hash: str,
        expires_at: datetime,
        ip_address: IPAddress | None = None,
        user_agent: str | None = None,
        device_name: str | None = None,
        last_seen_at: datetime | None = None,
    ) -> UserSession:
        """Create and persist a new user session."""

        user_session = UserSession(
            user_id=user_id,
            token_family_id=token_family_id,
            refresh_token_hash=refresh_token_hash,
            expires_at=expires_at,
            ip_address=ip_address,
            user_agent=user_agent,
            device_name=device_name,
            last_seen_at=last_seen_at,
        )

        self.session.add(user_session)

        await self.session.flush()
        await self.session.refresh(user_session)

        return user_session

    async def get_by_id(self, session_id: UUID) -> UserSession | None:
        """Return a session by its primary key."""

        stmt = select(UserSession).where(
            UserSession.id == session_id,
        )

        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_refresh_token_hash(
        self, refresh_token_hash: str
    ) -> UserSession | None:
        """Return a session by its refresh-token hash."""

        stmt = select(UserSession).where(
            UserSession.refresh_token_hash == refresh_token_hash,
        )

        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_token_family_id(self, token_family_id: UUID) -> list[UserSession]:
        """Return all sessions belonging to a token family."""

        stmt = (
            select(UserSession)
            .where(UserSession.token_family_id == token_family_id)
            .order_by(UserSession.created_at.desc())
        )

        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def get_by_user_id(self, user_id: UUID) -> list[UserSession]:
        """Return all sessions belonging to a user."""

        stmt = (
            select(UserSession)
            .where(UserSession.user_id == user_id)
            .order_by(UserSession.created_at.desc())
        )

        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def get_active_by_id(
        self, session_id: UUID, *, now: datetime
    ) -> UserSession | None:
        """Return an active, non-expired, non-revoked session."""

        stmt = select(UserSession).where(
            UserSession.id == session_id,
            UserSession.revoked_at.is_(None),
            UserSession.expires_at > now,
        )

        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_active_by_refresh_token_hash(
        self, refresh_token_hash: str, *, now: datetime
    ) -> UserSession | None:
        """Return an active session for a refresh-token hash."""

        stmt = select(UserSession).where(
            UserSession.refresh_token_hash == refresh_token_hash,
            UserSession.revoked_at.is_(None),
            UserSession.expires_at > now,
        )

        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def update_last_seen(
        self, session_id: UUID, *, last_seen_at: datetime
    ) -> bool:
        """Update the last-seen timestamp.

        Returns:
            True if a row was updated, otherwise False.
        """

        stmt = (
            update(UserSession)
            .where(UserSession.id == session_id)
            .values(last_seen_at=last_seen_at)
        )

        result = await self.session.execute(stmt)
        return result.rowcount > 0  # type: ignore

    async def revoke(self, session_id: UUID, *, revoked_at: datetime) -> bool:
        """Revoke a session.

        Returns:
            True if a row was updated, otherwise False.
        """

        stmt = (
            update(UserSession)
            .where(
                UserSession.id == session_id,
                UserSession.revoked_at.is_(None),
            )
            .values(revoked_at=revoked_at)
        )

        result = await self.session.execute(stmt)
        return result.rowcount > 0  # type: ignore

    async def revoke_by_token_family_id(
        self, token_family_id: UUID, *, revoked_at: datetime
    ) -> int:
        """Revoke every session belonging to a token family."""

        stmt = (
            update(UserSession)
            .where(
                UserSession.token_family_id == token_family_id,
                UserSession.revoked_at.is_(None),
            )
            .values(revoked_at=revoked_at)
        )

        result = await self.session.execute(stmt)
        return result.rowcount  # type: ignore

    async def revoke_all_for_user(self, user_id: UUID, *, revoked_at: datetime) -> int:
        """Revoke every active session belonging to a user."""

        stmt = (
            update(UserSession)
            .where(
                UserSession.user_id == user_id,
                UserSession.revoked_at.is_(None),
            )
            .values(revoked_at=revoked_at)
        )

        result = await self.session.execute(stmt)
        return result.rowcount  # type: ignore

    async def delete(self, session_id: UUID) -> bool:
        """Permanently delete a session."""

        stmt = delete(UserSession).where(
            UserSession.id == session_id,
        )

        result = await self.session.execute(stmt)
        return result.rowcount > 0  # type: ignore

    async def delete_expired(self, *, before: datetime) -> int:
        """Delete sessions that have expired before the given timestamp."""

        stmt = delete(UserSession).where(
            UserSession.expires_at < before,
        )

        result = await self.session.execute(stmt)
        return result.rowcount  # type: ignore

    async def delete_revoked(self, *, before: datetime) -> int:
        """Delete revoked sessions whose revocation time is older than the given timestamp."""

        stmt = delete(UserSession).where(
            UserSession.revoked_at.is_not(None),
            UserSession.revoked_at < before,
        )

        result = await self.session.execute(stmt)
        return result.rowcount  # type: ignore
