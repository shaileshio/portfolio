import pytest
from httpx import AsyncClient

from app.db.models.user import User
from tests.schemas.users import UserCredentials

pytestmark = [
    pytest.mark.api,
    pytest.mark.auth,
    pytest.mark.register,
]


async def test_register_returns_422_when_required_fields_missing(
    client: AsyncClient,
) -> None:
    response = await client.post("/api/v1/auth/register", json={})

    assert response.status_code == 422


async def test_register_returns_400_when_password_missmatch(
    client: AsyncClient, user_credentials: UserCredentials
) -> None:
    response = await client.post(
        "/api/v1/auth/register",
        json={
            "email": user_credentials.email,
            "password": user_credentials.password,
            "confirm_password": "password-missmatch",
        },
    )

    assert response.status_code == 400


async def test_register_returns_409_when_already_email_exists(
    client: AsyncClient, created_user: User
) -> None:
    response = await client.post(
        "/api/v1/auth/register",
        json={
            "email": created_user.email,
            "password": "...",
            "confirm_password": "...",
        },
    )

    assert response.status_code == 409


async def test_register_success(
    client: AsyncClient, user_credentials: UserCredentials
) -> None:
    response = await client.post(
        "/api/v1/auth/register",
        json={
            "email": user_credentials.email,
            "password": user_credentials.password,
            "confirm_password": user_credentials.password,
        },
    )

    assert response.status_code == 200
