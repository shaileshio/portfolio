from collections.abc import Mapping
from datetime import datetime
from typing import Any

from jose import jwt
from uuid6 import uuid6

from app.shared.datetime import get_utc_now


def create_token(
    *,
    subject: str,
    claims: Mapping[str, Any],
    expires_at: datetime,
    secret_key: str,
    algorithm: str,
) -> str:

    payload: dict[str, Any] = {
        **claims,
        "sub": subject,
        "jti": str(uuid6()),
        "iat": get_utc_now(),
        "exp": expires_at,
    }

    return jwt.encode(claims=payload, key=secret_key, algorithm=algorithm)
