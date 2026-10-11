from collections.abc import AsyncGenerator

import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import (
    AsyncSession,
)

from app.db.models import User
from app.db.session import get_async_session
from app.main import app
from app.shared.depends import get_current_user


@pytest_asyncio.fixture
async def client(
    session: AsyncSession, mock_current_user: User
) -> AsyncGenerator[AsyncClient]:

    async def override_get_session() -> AsyncGenerator[AsyncSession]:
        yield session

    async def override_mock_current_user() -> User:
        return mock_current_user

    app.dependency_overrides[get_async_session] = override_get_session
    app.dependency_overrides[get_current_user] = override_mock_current_user

    try:
        async with AsyncClient(
            transport=ASGITransport(app=app),
            base_url="http://test",
        ) as client:
            yield client

    finally:
        app.dependency_overrides.pop(get_async_session, None)
        app.dependency_overrides.pop(get_current_user, None)
