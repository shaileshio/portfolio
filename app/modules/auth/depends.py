from typing import Annotated

from fastapi import Depends

from app.db.depends import AsyncSessionDep
from app.db.repositories.user import UserRepository
from app.db.repositories.user_session import UserSessionRepository

from .service import AuthService


def get_auth_service(session: AsyncSessionDep) -> AuthService:
    return AuthService(session, UserRepository(session), UserSessionRepository(session))


type AuthServiceDep = Annotated[AuthService, Depends(get_auth_service)]
