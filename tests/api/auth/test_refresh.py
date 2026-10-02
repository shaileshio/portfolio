import pytest
from httpx import AsyncClient

pytestmark = [
    pytest.mark.api,
    pytest.mark.auth,
]


@pytest.mark.refresh
async def test_invalid_refresh_token(async_client: AsyncClient) -> None:
    response = await async_client.post(
        "/api/v1/auth/refresh",
        json={"refresh_token": "invalid-refresh-token"},
    )

    assert response.status_code == 400
