from collections.abc import Mapping
from datetime import datetime
from typing import Any

from jose import jwt
from uuid6 import uuid7


def create_token(
    *,
    subject: str,
    claims: Mapping[str, Any],
    issue_at: datetime,
    expires_at: datetime,
    secret_key: str,
    algorithm: str,
) -> str:

    payload: dict[str, Any] = {
        **claims,
        "sub": subject,
        "jti": str(uuid7()),
        "iat": issue_at,
        "exp": expires_at,
    }

    return jwt.encode(claims=payload, key=secret_key, algorithm=algorithm)
