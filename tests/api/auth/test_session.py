import pytest
from faker import Faker
from httpx import AsyncClient

from app.db.models.user._user import User

pytestmark = [
    pytest.mark.api,
    pytest.mark.auth,
    pytest.mark.session,
]


async def test_list_sessions_empty(client: AsyncClient) -> None:
    list_sessions_response = await client.get(
        "/api/v1/auth/sessions",
    )

    assert list_sessions_response.status_code == 200
    assert len(list_sessions_response.json()["sessions"]) == 0


async def test_list_sessions_success(
    client: AsyncClient, user: User, password: str
) -> None:

    login_response = await client.post(
        "/api/v1/auth/login",
        json={"email": user.email, "password": password},
    )

    list_sessions_response = await client.get(
        "/api/v1/auth/sessions",
    )

    assert login_response.status_code == 200

    assert list_sessions_response.status_code == 200
    assert len(list_sessions_response.json()["sessions"]) > 0


async def test_get_session_with_invalid_id(client: AsyncClient, faker: Faker) -> None:

    retrieve_session_response = await client.get(
        f"/api/v1/auth/sessions/{faker.uuid7()}",
    )

    assert retrieve_session_response.status_code == 404


async def test_get_session_success(
    client: AsyncClient, user: User, password: str
) -> None:

    login_response = await client.post(
        "/api/v1/auth/login",
        json={"email": user.email, "password": password},
    )

    list_sessions_response = await client.get(
        "/api/v1/auth/sessions",
    )

    session_id: str = list_sessions_response.json()["sessions"][0]["id"]

    retrieve_session_response = await client.get(
        f"/api/v1/auth/sessions/{session_id}",
    )

    assert login_response.status_code == 200

    assert list_sessions_response.status_code == 200
    assert len(list_sessions_response.json()["sessions"]) > 0

    assert retrieve_session_response.json()["id"] == session_id
