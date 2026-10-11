import pytest
from httpx import AsyncClient

from tests.schemas.users import UserCredentials

pytestmark = [
    pytest.mark.e2e,
    pytest.mark.slow,
    pytest.mark.auth_workflow,
]


async def test_auth_workflow(
    client: AsyncClient, user_credentials: UserCredentials
) -> None:
    register = await client.post(
        "/api/v1/auth/register",
        json={
            "email": user_credentials.email,
            "password": user_credentials.password,
            "confirm_password": user_credentials.password,
        },
    )

    assert register.status_code == 200

    login = await client.post(
        "/api/v1/auth/login",
        json={
            "email": user_credentials.email,
            "password": user_credentials.password,
        },
    )

    assert login.status_code == 200

    refresh_token = login.json()["refresh_token"]

    refresh = await client.post(
        "/api/v1/auth/refresh",
        json={
            "refresh_token": refresh_token,
        },
    )

    assert refresh.status_code == 200

    logout = await client.post(
        "/api/v1/auth/logout",
        json={
            "refresh_token": refresh_token,
        },
    )

    assert logout.status_code == 200
