# tests/conftest.py

import pytest
import pytest_asyncio
from faker import Faker
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security.hashing.providers import get_hasher
from app.db.models import User


@pytest.fixture
def password() -> str:
    return "password@12345"


@pytest_asyncio.fixture
async def user(session: AsyncSession, faker: Faker, password: str) -> User:

    email = faker.unique.email()
    hasher = get_hasher()

    passowrd = hasher.hash(password)
    user = User(email=email, password_hash=passowrd)

    session.add(user)

    await session.commit()
    await session.refresh(user)

    return user
