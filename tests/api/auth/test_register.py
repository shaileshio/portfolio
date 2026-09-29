import pytest
from faker import Faker
from httpx import AsyncClient

from app.db.models.user import User

pytestmark = [
    pytest.mark.api,
    pytest.mark.auth,
]


@pytest.mark.register
async def test_register_password_missmatch(
    faker: Faker, async_client: AsyncClient
) -> None:
    email = faker.unique.email()
    password = faker.password()

    response = await async_client.post(
        "/api/v1/auth/register",
        json={
            "email": email,
            "password": password,
            "confirm_password": "not-equal-to-password",
        },
    )

    assert response.status_code == 400


@pytest.mark.register
async def test_register_success(faker: Faker, async_client: AsyncClient) -> None:
    email = faker.unique.email()
    password = faker.password()

    response = await async_client.post(
        "/api/v1/auth/register",
        json={
            "email": email,
            "password": password,
            "confirm_password": password,
        },
    )

    assert response.status_code == 200


@pytest.mark.register
async def test_register_email_exists(user: User, async_client: AsyncClient) -> None:
    response = await async_client.post(
        "/api/v1/auth/register",
        json={
            "email": user.email,
            "password": "...",
            "confirm_password": "...",
        },
    )

    assert response.status_code == 409
