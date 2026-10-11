import pytest
from httpx import AsyncClient

from app.db.models import User
from tests.schemas.users import UserCredentials

pytestmark = [
    pytest.mark.api,
    pytest.mark.auth,
    pytest.mark.login,
]


async def test_login_returns_422_when_required_fields_missing(
    client: AsyncClient,
) -> None:
    response = await client.post("/api/v1/auth/login", json={})

    assert response.status_code == 422


async def test_login_returns_404_when_email_address_not_exist(
    client: AsyncClient, user_credentials: UserCredentials, password: str
) -> None:
    response = await client.post(
        "/api/v1/auth/login",
        json={
            "email": user_credentials.email,
            "password": password,
        },
    )

    assert response.status_code == 404


async def test_login_returns_400_when_wrong_password(
    client: AsyncClient, created_user: User
) -> None:
    response = await client.post(
        "/api/v1/auth/login",
        json={
            "email": created_user.email,
            "password": "wrong-password",
        },
    )

    assert response.status_code == 400


async def test_login_success(
    client: AsyncClient, created_user: User, password: str
) -> None:
    response = await client.post(
        "/api/v1/auth/login",
        json={"email": created_user.email, "password": password},
    )

    assert response.status_code == 200
