from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.database.models.refresh_token import RefreshToken
from app.database.repositories.base import BaseRepository


class RefreshTokenRepository(BaseRepository[RefreshToken]):
    def __init__(self):
        super().__init__(RefreshToken)

    async def get_by_user(
        self,
        session: AsyncSession,
        user_id,
    ):
        statement = (
            select(RefreshToken)
            .where(RefreshToken.user_id == user_id)
        )

        result = await session.exec(statement)

        return result.all()

    async def get_by_token_hash(
        self,
        session: AsyncSession,
        token_hash: str,
    ) -> RefreshToken | None:
        statement = (
            select(RefreshToken)
            .where(RefreshToken.token_hash == token_hash)
        )

        result = await session.exec(statement)

        return result.first()
