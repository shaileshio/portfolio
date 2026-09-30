from collections.abc import Mapping
from datetime import datetime
from typing import Any

from app.core.config import get_settings

from .factory import create_token
from .verifier import TokenVerifier

settings = get_settings()


class TokenManager:
    def __init__(self, verifier: TokenVerifier) -> None:
        self.secret_key = settings.token.secret_key
        self.algorithm = settings.token.algorithm
        self.verifier = verifier

    def create(
        self, *, subject: str, expires_at: datetime, claims: Mapping[str, Any]
    ) -> str:
        return create_token(
            subject=subject,
            claims=claims,
            expires_at=expires_at,
            secret_key=self.secret_key,
            algorithm=self.algorithm,
        )

    def verify(self, *, token: str, subject: str) -> dict[str, Any]:
        return self.verifier.verify_token(
            token=token,
            subject=subject,
            secret_key=self.secret_key,
            algorithm=self.algorithm,
        )
