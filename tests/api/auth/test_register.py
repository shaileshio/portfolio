import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.user import User


@pytest.mark.api
@pytest.mark.auth
async def test_register_password_missmatch(async_client: AsyncClient) -> None:
    response = await async_client.post(
        "/auth/register",
        json={
            "email": "shailesh@gmail.com",
            "password": "shailesh@12345",
            "confirm_password": "shailesh@12",
        },
    )

    assert response.status_code == 400


@pytest.mark.api
@pytest.mark.auth
async def test_register_success(async_client: AsyncClient) -> None:
    response = await async_client.post(
        "/auth/register",
        json={
            "email": "shailesh@gmail.com",
            "password": "shailesh@12345",
            "confirm_password": "shailesh@12345",
        },
    )

    assert response.status_code == 200


@pytest.mark.api
@pytest.mark.auth
async def test_register_email_exists(
    async_client: AsyncClient, async_session: AsyncSession
) -> None:
    user = User(email="shailesh@gmail.com", password_hash="shailesh@12345")

    async_session.add(user)
    await async_session.flush()

    response = await async_client.post(
        "/auth/register",
        json={
            "email": "shailesh@gmail.com",
            "password": "shailesh@12345",
            "confirm_password": "shailesh@12345",
        },
    )

    assert response.status_code == 409
