import pytest
from httpx import AsyncClient

pytestmark = [
    pytest.mark.api,
    pytest.mark.health,
]


async def test_health_live(client: AsyncClient) -> None:
    response = await client.get("/health/live")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


async def test_health_ready(client: AsyncClient) -> None:
    response = await client.get("/health/ready")

    assert response.status_code == 200
    assert response.json() == {"status": "ok", "database": "connected"}
