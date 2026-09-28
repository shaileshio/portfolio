from sqlalchemy import exists, select
from sqlalchemy.ext.asyncio import AsyncSession

from ..models import User


class UserRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def email_exists(self, email: str) -> bool:
        stmt = select(exists().where(User.email == email))
        return bool(await self.session.scalar(stmt))

    async def create(self, email: str, password_hash: str) -> User:
        user = User(email=email, password_hash=password_hash, is_active=True)

        self.session.add(user)
        await self.session.flush()

        return user

    async def get_by_email(self, email: str) -> User | None:
        stmt = select(User).where(
            User.email == email,
            User.is_active == True,
        )

        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()
