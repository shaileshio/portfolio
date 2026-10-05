import pytest
from faker import Faker
from httpx import AsyncClient

from app.db.models import User

pytestmark = [
    pytest.mark.api,
    pytest.mark.auth,
    pytest.mark.login,
]


async def test_login_email_not_found(client: AsyncClient, faker: Faker) -> None:
    email = faker.unique.email()
    password = faker.password()

    response = await client.post(
        "/api/v1/auth/login",
        json={"email": email, "password": password},
    )

    assert response.status_code == 404


async def test_login_invalid_password(client: AsyncClient, user: User) -> None:
    response = await client.post(
        "/api/v1/auth/login",
        json={"email": user.email, "password": "wrong-password"},
    )

    assert response.status_code == 400


async def test_login_success(client: AsyncClient, user: User, password: str) -> None:
    response = await client.post(
        "/api/v1/auth/login",
        json={"email": user.email, "password": password},
    )

    assert response.status_code == 200
