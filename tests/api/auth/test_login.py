import pytest
from httpx import AsyncClient

from app.db.models.user._user import User

pytestmark = [
    pytest.mark.api,
    pytest.mark.auth,
]


@pytest.mark.login
async def test_login_email_not_found(async_client: AsyncClient) -> None:
    response = await async_client.post(
        "/auth/login",
        json={"email": "random@gmail.com", "password": "random@12345"},
    )

    assert response.status_code == 404


@pytest.mark.login
async def test_login_invalid_password(user: User, async_client: AsyncClient) -> None:
    response = await async_client.post(
        "/auth/login",
        json={"email": user.email, "password": "wrong-password"},
    )

    assert response.status_code == 400
