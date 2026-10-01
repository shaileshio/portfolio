from datetime import UTC, datetime
from ipaddress import IPv4Address, IPv6Address
from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import DateTime, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import INET
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.db.types import CreatedAt, UUID7PrimaryKey

if TYPE_CHECKING:
    from ._user import User


class UserSession(Base, name="user_sessions"):
    id: Mapped[UUID7PrimaryKey]

    user_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="SET NULL"),
        index=True,
    )

    refresh_token_hash: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        unique=True,
    )

    created_at: Mapped[CreatedAt]

    last_seen_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
    )

    refresh_expires_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        index=True,
    )

    session_expires_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        index=True,
    )

    revoked_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        index=True,
    )

    ip_address: Mapped[IPv4Address | IPv6Address | None] = mapped_column(
        INET,
    )

    user_agent: Mapped[str | None] = mapped_column(
        Text,
    )

    device_name: Mapped[str | None] = mapped_column(
        String(100),
    )

    user: Mapped[User] = relationship(back_populates="sessions")

    @property
    def is_revoked(self) -> bool:
        return self.revoked_at is not None

    def is_session_expired(self, *, now: datetime | None = None) -> bool:
        now = now or datetime.now(UTC)
        return now >= self.session_expires_at

    def is_refresh_expired(self, *, now: datetime | None = None) -> bool:
        now = now or datetime.now(UTC)
        return now >= self.refresh_expires_at

    def is_active(self, *, now: datetime | None = None) -> bool:
        return not self.is_revoked and not self.is_session_expired(now=now)

    def can_refresh(self, *, now: datetime | None = None) -> bool:
        return self.is_active(now=now)

    def touch(self, *, now: datetime | None = None) -> None:
        self.last_seen_at = now or datetime.now(UTC)

    def revoke(self, *, now: datetime | None = None) -> None:
        if self.revoked_at is None:
            self.revoked_at = now or datetime.now(UTC)
