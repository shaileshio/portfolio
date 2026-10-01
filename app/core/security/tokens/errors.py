from app.core.exceptions import AppError


class TokenError(AppError):
    def __init__(self, detail: str) -> None:
        super().__init__(detail)


class InvalidTokenError(TokenError):
    def __init__(self, detail: str = "Invalid token") -> None:
        super().__init__(detail)


class ExpiredTokenSignatureError(TokenError):
    def __init__(self, detail: str = "Token signature expire") -> None:
        super().__init__(detail)
