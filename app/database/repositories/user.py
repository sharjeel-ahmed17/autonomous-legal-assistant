from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.database.models.user import User
from app.database.repositories.base import BaseRepository


class UserRepository(BaseRepository[User]):
    def __init__(self):
        super().__init__(User)

    async def get_by_email(
        self,
        session: AsyncSession,
        email: str,
    ) -> User | None:
        statement = select(User).where(User.email == email)
        result = await session.exec(statement)
        return result.first()

    async def email_exists(
        self,
        session: AsyncSession,
        email: str,
    ) -> bool:
        return await self.get_by_email(session, email) is not None