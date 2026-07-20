from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.database.models.role import Role
from app.database.repositories.base import BaseRepository


class RoleRepository(BaseRepository[Role]):
    def __init__(self):
        super().__init__(Role)

    async def get_by_name(
        self,
        session: AsyncSession,
        name: str,
    ) -> Role | None:
        statement = (
            select(Role)
            .where(Role.name == name)
        )

        result = await session.exec(statement)

        return result.first()

    async def get_by_codename(
        self,
        session: AsyncSession,
        codename: str,
    ) -> Role | None:
        statement = (
            select(Role)
            .where(Role.codename == codename)
        )

        result = await session.exec(statement)

        return result.first()
