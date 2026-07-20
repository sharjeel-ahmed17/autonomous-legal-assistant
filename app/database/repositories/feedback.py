from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.database.models.feedback import Feedback
from app.database.repositories.base import BaseRepository


class FeedbackRepository(BaseRepository[Feedback]):
    def __init__(self):
        super().__init__(Feedback)

    async def get_by_user(
        self,
        session: AsyncSession,
        user_id,
    ):
        statement = (
            select(Feedback)
            .where(Feedback.user_id == user_id)
        )

        result = await session.exec(statement)

        return result.all()

    async def get_by_message(
        self,
        session: AsyncSession,
        message_id,
    ):
        statement = (
            select(Feedback)
            .where(Feedback.message_id == message_id)
        )

        result = await session.exec(statement)

        return result.all()

    async def get_by_agent_run(
        self,
        session: AsyncSession,
        agent_run_id,
    ):
        statement = (
            select(Feedback)
            .where(Feedback.agent_run_id == agent_run_id)
        )

        result = await session.exec(statement)

        return result.all()
