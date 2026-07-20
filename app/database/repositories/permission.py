from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.database.models.permission import Permission
from app.database.repositories.base import BaseRepository


class PermissionRepository(BaseRepository[Permission]):
    def __init__(self):
        super().__init__(Permission)

    async def get_by_name(
        self,
        session: AsyncSession,
        name: str,
    ) -> Permission | None:
        statement = (
            select(Permission)
            .where(Permission.name == name)
        )

        result = await session.exec(statement)

        return result.first()

    async def get_by_codename(
        self,
        session: AsyncSession,
        codename: str,
    ) -> Permission | None:
        statement = (
            select(Permission)
            .where(Permission.codename == codename)
        )

        result = await session.exec(statement)

        return result.first()
