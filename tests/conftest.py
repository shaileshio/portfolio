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
from app.db.session import get_async_session
from app.main import app

from .fixtures import *

settings = get_settings()

TEST_DATABASE_URL = settings.database.get_test_url()

type AsyncSessionGenerator = AsyncGenerator[AsyncSession]


@pytest_asyncio.fixture
async def async_engine() -> AsyncGenerator[AsyncEngine]:
    engine = create_async_engine(TEST_DATABASE_URL, echo=False, pool_pre_ping=True)

    try:
        yield engine
    finally:
        await engine.dispose()


@pytest_asyncio.fixture
async def async_connection(
    async_engine: AsyncEngine,
) -> AsyncGenerator[AsyncConnection]:
    async with async_engine.connect() as connection:
        transaction = await connection.begin()

        try:
            yield connection
        finally:
            if transaction.is_active:
                await transaction.rollback()


@pytest_asyncio.fixture
async def async_session(async_connection: AsyncConnection) -> AsyncSessionGenerator:
    async with AsyncSession(
        bind=async_connection,
        expire_on_commit=False,
        join_transaction_mode="create_savepoint",
    ) as session:
        yield session


@pytest_asyncio.fixture
async def async_client(async_session: AsyncSession) -> AsyncGenerator[AsyncClient]:
    async def override_get_async_session() -> AsyncSessionGenerator:
        yield async_session

    app.dependency_overrides[get_async_session] = override_get_async_session

    try:
        async with AsyncClient(
            transport=ASGITransport(app=app),
            base_url="http://test/api/v1",
        ) as client:
            yield client

    finally:
        app.dependency_overrides.pop(get_async_session, None)
