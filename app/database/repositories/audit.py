from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.database.models.audit import AuditLog
from app.database.repositories.base import BaseRepository


class AuditRepository(BaseRepository[AuditLog]):
    def __init__(self):
        super().__init__(AuditLog)

    async def get_user_logs(
        self,
        session: AsyncSession,
        user_id,
    ):
        statement = (
            select(AuditLog)
            .where(AuditLog.user_id == user_id)
        )

        result = await session.exec(statement)

        return result.all()