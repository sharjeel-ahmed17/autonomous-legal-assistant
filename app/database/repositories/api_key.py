from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.database.models.api_key import ApiKey
from app.database.repositories.base import BaseRepository


class ApiKeyRepository(BaseRepository[ApiKey]):
    def __init__(self):
        super().__init__(ApiKey)

    async def get_by_user(
        self,
        session: AsyncSession,
        user_id,
    ):
        statement = (
            select(ApiKey)
            .where(ApiKey.user_id == user_id)
        )

        result = await session.exec(statement)

        return result.all()

    async def get_by_key_hash(
        self,
        session: AsyncSession,
        key_hash: str,
    ) -> ApiKey | None:
        statement = (
            select(ApiKey)
            .where(ApiKey.key_hash == key_hash)
        )

        result = await session.exec(statement)

        return result.first()
