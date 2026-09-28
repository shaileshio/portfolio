from typing import TYPE_CHECKING

from sqlalchemy import Boolean, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.db.types import CreatedAt, UpdatedAt, UUID7PrimaryKey

if TYPE_CHECKING:
    from ..portfolio import Portfolio
    from .session import UserSession


class User(Base, name="users"):
    id: Mapped[UUID7PrimaryKey]

    email: Mapped[str] = mapped_column(
        String(length=320),
        nullable=False,
        unique=True,
        index=True,
    )

    password_hash: Mapped[str] = mapped_column(
        String(length=255),
        nullable=False,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )

    is_verified: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    created_at: Mapped[CreatedAt]
    updated_at: Mapped[UpdatedAt]

    sessions: Mapped[list[UserSession]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

    portfolios: Mapped[list[Portfolio]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
    )
