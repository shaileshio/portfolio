import pytest
import pytest_asyncio
from faker import Faker
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security.hashing.providers import get_hasher
from app.db.models import User
from tests.schemas.users import UserCredentials


@pytest.fixture
def password() -> str:
    return "password@12345"


@pytest.fixture
def user_credentials(faker: Faker, password: str) -> UserCredentials:
    return UserCredentials(
        email=faker.unique.email(),
        password=password,
    )


@pytest_asyncio.fixture
async def created_user(
    session: AsyncSession, user_credentials: UserCredentials
) -> User:
    user = User(
        email=user_credentials.email,
        password_hash=get_hasher().hash(user_credentials.password),
    )

    session.add(user)

    await session.commit()
    await session.refresh(user)

    return user
