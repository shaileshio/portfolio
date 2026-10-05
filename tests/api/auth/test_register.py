import pytest
from faker import Faker
from httpx import AsyncClient

from app.db.models.user import User

pytestmark = [
    pytest.mark.api,
    pytest.mark.auth,
    pytest.mark.register,
]


async def test_register_password_missmatch(client: AsyncClient, faker: Faker) -> None:
    email = faker.unique.email()
    password = faker.password()

    response = await client.post(
        "/api/v1/auth/register",
        json={
            "email": email,
            "password": password,
            "confirm_password": "not-equal-to-password",
        },
    )

    assert response.status_code == 400


async def test_register_success(client: AsyncClient, faker: Faker) -> None:
    email = faker.unique.email()
    password = faker.password()

    response = await client.post(
        "/api/v1/auth/register",
        json={
            "email": email,
            "password": password,
            "confirm_password": password,
        },
    )

    assert response.status_code == 200


async def test_register_email_exists(client: AsyncClient, user: User) -> None:
    response = await client.post(
        "/api/v1/auth/register",
        json={
            "email": user.email,
            "password": "...",
            "confirm_password": "...",
        },
    )

    assert response.status_code == 409
