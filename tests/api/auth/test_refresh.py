import pytest
from httpx import AsyncClient

from app.db.models import User

pytestmark = [
    pytest.mark.api,
    pytest.mark.auth,
    pytest.mark.refresh,
]


async def test_refresh_returns_422_when_required_fields_missing(
    client: AsyncClient,
) -> None:
    response = await client.post("/api/v1/auth/refresh", json={})

    assert response.status_code == 422


async def test_refresh_returns_400_when_token_is_not_valid(client: AsyncClient) -> None:
    response = await client.post(
        "/api/v1/auth/refresh",
        json={"refresh_token": "invalid-refresh-token"},
    )

    assert response.status_code == 400


async def test_refresh_success(
    client: AsyncClient, created_user: User, password: str
) -> None:
    login_response = await client.post(
        "/api/v1/auth/login",
        json={"email": created_user.email, "password": password},
    )

    assert login_response.status_code == 200

    refresh_response = await client.post(
        "/api/v1/auth/refresh",
        json={"refresh_token": login_response.json()["refresh_token"]},
    )

    assert refresh_response.status_code == 200
