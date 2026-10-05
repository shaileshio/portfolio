import pytest
from faker import Faker
from httpx import AsyncClient

pytestmark = [
    pytest.mark.e2e,
    pytest.mark.slow,
    pytest.mark.auth_workflow,
]


async def test_auth_workflow(client: AsyncClient, faker: Faker) -> None:
    email = faker.unique.email()
    password = faker.password()

    register = await client.post(
        "/api/v1/auth/register",
        json={
            "email": email,
            "password": password,
            "confirm_password": password,
        },
    )

    login = await client.post(
        "/api/v1/auth/login",
        json={
            "email": email,
            "password": password,
        },
    )

    refresh_token = login.json()["refresh_token"]

    refresh = await client.post(
        "/api/v1/auth/refresh",
        json={
            "refresh_token": refresh_token,
        },
    )

    logout = await client.post(
        "/api/v1/auth/logout",
        json={
            "refresh_token": refresh_token,
        },
    )

    assert register.status_code == 200
    assert login.status_code == 200
    assert refresh.status_code == 200
    assert logout.status_code == 200
