import pytest
from faker import Faker
from httpx import AsyncClient

from app.db.models.user._user import User

pytestmark = [
    pytest.mark.api,
    pytest.mark.auth,
]


@pytest.mark.login
async def test_login_email_not_found(async_client: AsyncClient, faker: Faker) -> None:
    email = faker.unique.email()
    password = faker.password()

    response = await async_client.post(
        "/api/v1/auth/login",
        json={"email": email, "password": password},
    )

    assert response.status_code == 404


@pytest.mark.login
async def test_login_invalid_password(async_client: AsyncClient, user: User) -> None:
    response = await async_client.post(
        "/api/v1/auth/login",
        json={"email": user.email, "password": "wrong-password"},
    )

    assert response.status_code == 400


@pytest.mark.login
async def test_login_success(
    async_client: AsyncClient, user: User, password: str
) -> None:
    response = await async_client.post(
        "/api/v1/auth/login",
        json={"email": user.email, "password": password},
    )

    assert response.status_code == 200
