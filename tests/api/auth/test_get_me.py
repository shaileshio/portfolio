import pytest
from httpx import AsyncClient

pytestmark = [
    pytest.mark.api,
    pytest.mark.auth,
]


@pytest.mark.me
async def test_get_me_success(async_client: AsyncClient) -> None:
    response = await async_client.get("/api/v1/auth/me")

    assert response.status_code == 200
