import pytest
from httpx import AsyncClient


@pytest.mark.api
@pytest.mark.health
async def test_health_live(async_client: AsyncClient) -> None:
    response = await async_client.get("/health/live")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


@pytest.mark.api
@pytest.mark.health
async def test_health_ready(async_client: AsyncClient) -> None:
    response = await async_client.get("/health/ready")

    assert response.status_code == 200
    assert response.json() == {"status": "ok", "database": "connected"}
