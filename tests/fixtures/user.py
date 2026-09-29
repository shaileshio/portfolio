# tests/conftest.py

import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security.hashing.providers import get_hasher
from app.db.models import User


@pytest_asyncio.fixture
async def user(async_session: AsyncSession) -> User:
    hasher = get_hasher()

    passowrd = hasher.hash("user@12345")
    user = User(email="user@example.com", password_hash=passowrd)

    async_session.add(user)
    await async_session.commit()
    await async_session.refresh(user)

    return user
