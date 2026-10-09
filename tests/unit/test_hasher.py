import pytest

from app.core.security.hashing import get_hasher

pytestmark = [
    pytest.mark.unit,
    pytest.mark.hasher,
]


def test_hash_success() -> None:
    hasher = get_hasher()

    value = hasher.hash("shailesh")
    assert hasher.verify("shailesh", value)


def test_hash_failed() -> None:
    hasher = get_hasher()

    value = hasher.hash("john")
    assert not hasher.verify("me", value)
