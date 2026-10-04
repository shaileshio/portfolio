import pytest

from app.db.models import User


@pytest.fixture
def mock_current_user(user: User) -> User:
    return user
