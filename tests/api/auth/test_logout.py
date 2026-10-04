import pytest
from httpx import AsyncClient

from app.db.models.user._user import User

pytestmark = [
    pytest.mark.api,
    pytest.mark.auth,
]


@pytest.mark.logout
async def test_logout_field_required(client: AsyncClient) -> None:
    response = await client.post(
        "/api/v1/auth/logout",
        json={},
    )

    assert response.status_code == 422


@pytest.mark.logout
async def test_logout_invalid_token(client: AsyncClient) -> None:
    response = await client.post(
        "/api/v1/auth/logout",
        json={"refresh_token": "invalid-refresh-token"},
    )

    assert response.status_code == 400


@pytest.mark.logout
async def test_logout_success(client: AsyncClient, user: User, password: str) -> None:

    login_response = await client.post(
        "/api/v1/auth/login",
        json={"email": user.email, "password": password},
    )

    logout_response = await client.post(
        "/api/v1/auth/logout",
        json={"refresh_token": login_response.json()["refresh_token"]},
    )

    assert login_response.status_code == 200
    assert logout_response.status_code == 200
