import pytest
from faker import Faker
from httpx import AsyncClient

from tests.schemas.auth import AuthCredentials

pytestmark = [
    pytest.mark.api,
    pytest.mark.auth,
    pytest.mark.session,
]


async def test_list_sessions_with_zero_records(client: AsyncClient) -> None:
    response = await client.get("/api/v1/auth/sessions")

    assert response.status_code == 200
    assert len(response.json()["sessions"]) == 0


async def test_list_sessions_success(
    client: AsyncClient,
    auth_credentials: AuthCredentials,
    password: str,
) -> None:
    login_response = await client.post(
        "/api/v1/auth/login",
        json={"email": auth_credentials.email, "password": password},
    )

    assert login_response.status_code == 200

    list_sessions_response = await client.get(
        "/api/v1/auth/sessions",
    )

    assert list_sessions_response.status_code == 200
    assert len(list_sessions_response.json()["sessions"]) > 0


async def test_get_session_returns_404_when_invalid_session_id(
    client: AsyncClient, faker: Faker
) -> None:
    response = await client.get(f"/api/v1/auth/sessions/{faker.uuid7()}")

    assert response.status_code == 404


async def test_get_session_success(
    client: AsyncClient, auth_credentials: AuthCredentials, password: str
) -> None:
    login_response = await client.post(
        "/api/v1/auth/login",
        json={"email": auth_credentials.email, "password": password},
    )

    assert login_response.status_code == 200

    list_sessions_response = await client.get(
        "/api/v1/auth/sessions",
    )

    assert list_sessions_response.status_code == 200
    assert len(list_sessions_response.json()["sessions"]) > 0

    session_id: str = list_sessions_response.json()["sessions"][0]["id"]

    retrieve_session_response = await client.get(
        f"/api/v1/auth/sessions/{session_id}",
    )

    assert retrieve_session_response.status_code == 200
    assert retrieve_session_response.json()["id"] == session_id
