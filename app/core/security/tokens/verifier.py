from logging import getLogger
from typing import Any

from jose import ExpiredSignatureError, jwt
from jose import JWTError as JoseJWTError

from app.shared.datetime import get_utc_now

from .errors import ExpiredTokenSignatureError, InvalidTokenError, TokenExpiredError

logger = getLogger(__name__)


class TokenVerifier:
    def verify_token(
        self, *, token: str, secret_key: str, algorithm: str
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

        self._validate(claims)

        return claims

    @staticmethod
    def _validate(claims: dict[str, Any]) -> None:
        required = {"sub", "exp", "iat", "jti"}
        if not required.issubset(claims):
            raise InvalidTokenError

        ttl = max(claims["exp"] - int(get_utc_now().timestamp()), 0)

        if ttl < 0:
            raise TokenExpiredError
