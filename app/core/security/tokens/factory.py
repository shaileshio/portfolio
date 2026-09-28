from collections.abc import Mapping
from datetime import UTC, datetime, timedelta
from typing import Any

from jose import jwt
from uuid6 import uuid6


def create_token(
    *,
    subject: str,
    claims: Mapping[str, Any],
    secret_key: str,
    algorithm: str,
    expires_in: timedelta,
) -> str:
    utc_now = datetime.now(UTC)

    payload: dict[str, Any] = {
        **claims,
        "sub": subject,
        "jti": str(uuid6()),
        "iat": utc_now,
        "exp": utc_now + expires_in,
    }

    return jwt.encode(
        claims=payload,
        key=secret_key,
        algorithm=algorithm,
    )
