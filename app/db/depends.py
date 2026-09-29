from typing import Annotated

from fastapi import Depends

from .session import AsyncSession, get_async_session

type AsyncSessionDep = Annotated[AsyncSession, Depends(get_async_session)]
