from logging import getLogger
from typing import Any

from jose import ExpiredSignatureError, jwt
from jose import JWTError as JoseJWTError

from .errors import ExpiredTokenSignatureError, InvalidTokenError

logger = getLogger(__name__)


class TokenVerifier:
    def verify_token(
        self, *, token: str, subject: str, secret_key: str, algorithm: str
    ) -> dict[str, Any]:
        try:
            claims = jwt.decode(
                token=token,
                key=secret_key,
                algorithms=[algorithm],
            )
        except ExpiredSignatureError as exc:
            logger.debug("Expired Jwt", exc_info=exc)
            raise ExpiredTokenSignatureError

        except JoseJWTError as exc:
            logger.debug("Invalid Jwt", exc_info=exc)
            raise InvalidTokenError

        self._validate(subject, claims)
        return claims

    @staticmethod
    def _validate(subject: str, claims: dict[str, Any]) -> None:
        required = {"sub", "exp", "iat", "jti"}
        if not required.issubset(claims) and claims["sub"] != subject:
            raise InvalidTokenError
