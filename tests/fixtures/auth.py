import pytest
import pytest_asyncio
from faker import Faker
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security.hashing.providers import get_hasher
from app.db.models import User
from tests.schemas.auth import AuthCredentials


@pytest.fixture
def auth_credentials(faker: Faker, password: str) -> AuthCredentials:
    return AuthCredentials(
        email=faker.unique.email(),
        password=password,
    )


@pytest_asyncio.fixture
async def mock_current_user(
    session: AsyncSession, auth_credentials: AuthCredentials
) -> User:
    user = User(
        email=auth_credentials.email,
        password_hash=get_hasher().hash(auth_credentials.password),
    )

    session.add(user)

    await session.commit()
    await session.refresh(user)

    return user
