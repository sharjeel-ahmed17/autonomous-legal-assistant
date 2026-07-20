from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.database.models.message import Message
from app.database.repositories.base import BaseRepository


class MessageRepository(BaseRepository[Message]):
    def __init__(self):
        super().__init__(Message)

    async def get_conversation_messages(
        self,
        session: AsyncSession,
        conversation_id,
    ):
        statement = (
            select(Message)
            .where(Message.conversation_id == conversation_id)
        )

        result = await session.exec(statement)

        return result.all()