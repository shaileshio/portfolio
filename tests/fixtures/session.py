from collections.abc import AsyncGenerator

import pytest_asyncio
from sqlalchemy.ext.asyncio import (
    AsyncConnection,
    AsyncSession,
)


@pytest_asyncio.fixture
async def session(connection: AsyncConnection) -> AsyncGenerator[AsyncSession]:
    async with AsyncSession(
        bind=connection,
        expire_on_commit=False,
        join_transaction_mode="create_savepoint",
    ) as session:
        yield session
