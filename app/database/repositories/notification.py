from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.database.models.notification import Notification
from app.database.repositories.base import BaseRepository


class NotificationRepository(BaseRepository[Notification]):
    def __init__(self):
        super().__init__(Notification)

    async def get_by_user(
        self,
        session: AsyncSession,
        user_id,
    ):
        statement = (
            select(Notification)
            .where(Notification.user_id == user_id)
        )

        result = await session.exec(statement)

        return result.all()

    async def get_unread_by_user(
        self,
        session: AsyncSession,
        user_id,
    ):
        statement = (
            select(Notification)
            .where(Notification.user_id == user_id)
            .where(Notification.is_read == False)
        )

        result = await session.exec(statement)

        return result.all()
