from collections.abc import Mapping
from datetime import datetime
from typing import Any

from app.core.config import get_settings

from .factory import create_token
from .verifier import TokenVerifier

settings = get_settings()

secret_key = settings.auth.jwt_secret_key
algorithm = settings.auth.jwt_hashing_algorithm


class TokenManager:
    def __init__(self, verifier: TokenVerifier) -> None:
        self._secret_key = secret_key
        self._algorithm = algorithm
        self._verifier = verifier

    def create(
        self, *, subject: str, expires_at: datetime, claims: Mapping[str, Any]
    ) -> str:
        return create_token(
            subject=subject,
            claims=claims,
            expires_at=expires_at,
            secret_key=self._secret_key,
            algorithm=self._algorithm,
        )

    def verify(self, token: str) -> dict[str, Any]:
        return self._verifier.verify_token(
            token=token,
            secret_key=self._secret_key,
            algorithm=self._algorithm,
        )
