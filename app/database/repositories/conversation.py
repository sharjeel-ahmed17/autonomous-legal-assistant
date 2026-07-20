from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.database.models.conversation import Conversation
from app.database.repositories.base import BaseRepository


class ConversationRepository(BaseRepository[Conversation]):
    def __init__(self):
        super().__init__(Conversation)

    async def get_user_conversations(
        self,
        session: AsyncSession,
        user_id,
    ):
        statement = (
            select(Conversation)
            .where(Conversation.user_id == user_id)
        )

        result = await session.exec(statement)

        return result.all()