# tests/conftest.py

import pytest_asyncio
from faker import Faker
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security.hashing.providers import get_hasher
from app.db.models import User


@pytest_asyncio.fixture
async def user(faker: Faker, async_session: AsyncSession) -> User:
    email = faker.unique.email()
    raw_password = faker.password()

    hasher = get_hasher()

    passowrd = hasher.hash(raw_password)
    user = User(email=email, password_hash=passowrd)

    async_session.add(user)

    await async_session.commit()
    await async_session.refresh(user)

    return user
