from fastapi import status


class AppError(Exception):
    def __init__(self, detail: str) -> None:
        self.detail = detail

        super().__init__(detail)


class HttpError(AppError):
    def __init__(self, detail: str, *, code: str, status: int) -> None:
        self.code = code
        self.status = status

        super().__init__(detail)


class BadRequestError(HttpError):
    def __init__(
        self,
        detail: str = "Bad request",
        *,
        code: str = "bad_request",
        status: int = status.HTTP_400_BAD_REQUEST,
    ) -> None:
        super().__init__(detail, code=code, status=status)


class UnauthorizedError(HttpError):
    def __init__(
        self,
        detail: str = "Authentication required",
        *,
        code: str = "unauthorized",
        status: int = status.HTTP_401_UNAUTHORIZED,
    ) -> None:
        super().__init__(detail, code=code, status=status)


class ForbiddenError(HttpError):
    def __init__(
        self,
        detail: str = "Access denied",
        *,
        code: str = "forbidden",
        status: int = status.HTTP_403_FORBIDDEN,
    ) -> None:
        super().__init__(detail, code=code, status=status)


class NotFoundError(HttpError):
    def __init__(
        self,
        detail: str = "Resource not found",
        *,
        code: str = "not_found",
        status: int = status.HTTP_404_NOT_FOUND,
    ) -> None:
        super().__init__(detail, code=code, status=status)


class ConflictError(HttpError):
    def __init__(
        self,
        detail: str = "Resource conflict",
        *,
        code: str = "conflict",
        status: int = status.HTTP_409_CONFLICT,
    ) -> None:
        super().__init__(detail, code=code, status=status)
