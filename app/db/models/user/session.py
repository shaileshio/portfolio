from datetime import datetime
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
        ForeignKey(
            column="users.id",
            ondelete="SET NULL",
        ),
        index=True,
    )

    token_family_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        nullable=False,
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

    expires_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )

    revoked_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
    )

    ip_address: Mapped[IPv4Address | IPv6Address | None] = mapped_column(INET)

    user_agent: Mapped[str | None] = mapped_column(Text)

    device_name: Mapped[str | None] = mapped_column(
        String(100),
    )

    user: Mapped[User] = relationship(
        back_populates="sessions",
    )
