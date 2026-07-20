from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.database.models.agent_run import AgentRun
from app.database.repositories.base import BaseRepository


class AgentRunRepository(BaseRepository[AgentRun]):
    def __init__(self):
        super().__init__(AgentRun)

    async def get_by_user(
        self,
        session: AsyncSession,
        user_id,
    ):
        statement = (
            select(AgentRun)
            .where(AgentRun.user_id == user_id)
        )

        result = await session.exec(statement)

        return result.all()

    async def get_by_conversation(
        self,
        session: AsyncSession,
        conversation_id,
    ):
        statement = (
            select(AgentRun)
            .where(AgentRun.conversation_id == conversation_id)
        )

        result = await session.exec(statement)

        return result.all()

    async def get_by_status(
        self,
        session: AsyncSession,
        status: str,
    ):
        statement = (
            select(AgentRun)
            .where(AgentRun.status == status)
        )

        result = await session.exec(statement)

        return result.all()
