import pytest
from httpx import AsyncClient

from app.db.models.user._user import User

pytestmark = [
    pytest.mark.api,
    pytest.mark.auth,
    pytest.mark.logout,
]


async def test_logout_returns_422_when_required_fields_missing(
    client: AsyncClient,
) -> None:
    response = await client.post("/api/v1/auth/logout", json={})

    assert response.status_code == 422


async def test_logout_returns_400_when_token_is_not_valid(client: AsyncClient) -> None:
    response = await client.post(
        "/api/v1/auth/logout",
        json={"refresh_token": "invalid-refresh-token"},
    )

    assert response.status_code == 400


async def test_logout_success(
    client: AsyncClient, created_user: User, password: str
) -> None:
    login_response = await client.post(
        "/api/v1/auth/login",
        json={"email": created_user.email, "password": password},
    )

    assert login_response.status_code == 200

    response = await client.post(
        "/api/v1/auth/logout",
        json={"refresh_token": login_response.json()["refresh_token"]},
    )

    assert response.status_code == 200
