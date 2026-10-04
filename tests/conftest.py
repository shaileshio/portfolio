from collections.abc import AsyncGenerator

import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import (
    AsyncConnection,
    AsyncEngine,
    AsyncSession,
    create_async_engine,
)

from app.core.config import get_settings
from app.db.models import User
from app.db.session import get_async_session
from app.main import app
from app.shared.depends import get_current_user

from .fixtures import *

settings = get_settings()

TEST_DATABASE_URL = settings.database.get_test_url()

type AsyncSessionGenerator = AsyncGenerator[AsyncSession]


@pytest_asyncio.fixture
async def engine() -> AsyncGenerator[AsyncEngine]:
    engine = create_async_engine(
        TEST_DATABASE_URL,
        echo=False,
        pool_pre_ping=True,
    )

    try:
        yield engine
    finally:
        await engine.dispose()


@pytest_asyncio.fixture
async def connection(engine: AsyncEngine) -> AsyncGenerator[AsyncConnection]:
    async with engine.connect() as connection:
        transaction = await connection.begin()

        try:
            yield connection
        finally:
            if transaction.is_active:
                await transaction.rollback()


@pytest_asyncio.fixture
async def session(connection: AsyncConnection) -> AsyncSessionGenerator:
    async with AsyncSession(
        bind=connection,
        expire_on_commit=False,
        join_transaction_mode="create_savepoint",
    ) as session:
        yield session


@pytest_asyncio.fixture
async def client(
    session: AsyncSession, mock_current_user: User
) -> AsyncGenerator[AsyncClient]:

    async def override_get_session() -> AsyncSessionGenerator:
        yield session

    def override_mock_current_user() -> User:
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
