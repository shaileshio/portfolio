from fastapi import status

from app.core.exceptions import BadRequestError, ConflictError, NotFoundError


class ConfirmPasswordNotMatchError(BadRequestError):
    def __init__(
        self,
        detail: str = "Confirm password doesn't match",
        *,
        code: str = "confirm_password_not_match",
        status: int = status.HTTP_400_BAD_REQUEST,
    ) -> None:
        super().__init__(detail, code=code, status=status)


class UserNotFoundError(NotFoundError):
    def __init__(
        self,
        detail: str = "User not found",
        *,
        code: str = "user_not_found",
        status: int = status.HTTP_404_NOT_FOUND,
    ) -> None:
        super().__init__(detail, code=code, status=status)


class InvalidPasswordError(NotFoundError):
    def __init__(
        self,
        detail: str = "Invalid password",
        *,
        code: str = "invalid_password",
        status: int = status.HTTP_400_BAD_REQUEST,
    ) -> None:
        super().__init__(detail, code=code, status=status)


class EmailAlreadyExistError(ConflictError):
    def __init__(
        self,
        detail: str = "Email already exist",
        *,
        code: str = "email_exist",
        status: int = 409,
    ) -> None:
        super().__init__(detail, code=code, status=status)


class UserSessionNotFoundError(NotFoundError):
    def __init__(
        self,
        detail: str = "User session does't exist",
        *,
        code: str = "user_not_found",
        status: int = status.HTTP_404_NOT_FOUND,
    ) -> None:
        super().__init__(detail, code=code, status=status)


class InvalidRefreshTokenError(NotFoundError):
    def __init__(
        self,
        detail: str = "Invalid token type. Please provide refresh token",
        *,
        code: str = "invalid_password",
        status: int = status.HTTP_400_BAD_REQUEST,
    ) -> None:
        super().__init__(detail, code=code, status=status)
