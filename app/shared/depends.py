from typing import Annotated
from uuid import UUID

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from app.core.exceptions.errors import UnauthorizedError
from app.core.security.tokens import get_token_manager
from app.core.security.tokens.enum import TokenType
from app.db.depends import AsyncSessionDep
from app.db.models.user._user import User
from app.db.repositories.user import UserRepository
from app.db.repositories.user_session import UserSessionRepository
from app.modules.v1.auth.errors import InvalidTokenError

type OAuth2PasswordBearerDep = Annotated[
    str,
    Depends(
        OAuth2PasswordBearer(
            tokenUrl="/api/v1/auth/login",
            description="Use email as the username field",
        )
    ),
]


async def get_current_user(
    token: OAuth2PasswordBearerDep, session: AsyncSessionDep
) -> User:

    user_repo = UserRepository(session)
    user_session_repo = UserSessionRepository(session)

    claims = get_token_manager().verify(token)

    try:
        user_id = claims["sub"]
        session_id = claims["sid"]
    except KeyError:
        raise InvalidTokenError

    user = await user_repo.get_by_id(user_id)

    if user is None:
        raise UnauthorizedError

    user_session = await user_session_repo.get_by_ids(
        user_id=UUID(user_id), session_id=UUID(session_id)
    )

    if claims["type"] != TokenType.ACCESS.value or not user_session:
        raise InvalidTokenError

    return user


type CurrentUserDep = Annotated[User, Depends(get_current_user)]
