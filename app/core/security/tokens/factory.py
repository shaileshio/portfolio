from collections.abc import Mapping
from datetime import UTC, datetime, timedelta
from typing import Any
from uuid import uuid4

from jose import jwt


def create_token(
    *,
    claims: Mapping[str, Any],
    subject: str,
    secret_key: str,
    algorithm: str,
    expires_in: timedelta,
) -> str:
    utc_now = datetime.now(UTC)

    payload: dict[str, Any] = {
        **claims,
        "sub": subject,
        "jti": str(uuid4()),
        "iat": utc_now,
        "exp": utc_now + expires_in,
    }

    return jwt.encode(
        claims=payload,
        key=secret_key,
        algorithm=algorithm,
    )
