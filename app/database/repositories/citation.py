from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.database.models.citation import Citation
from app.database.repositories.base import BaseRepository


class CitationRepository(BaseRepository[Citation]):
    def __init__(self):
        super().__init__(Citation)

    async def get_by_document(
        self,
        session: AsyncSession,
        document_id,
    ):
        statement = (
            select(Citation)
            .where(Citation.document_id == document_id)
        )

        result = await session.exec(statement)

        return result.all()

    async def get_by_message(
        self,
        session: AsyncSession,
        message_id,
    ):
        statement = (
            select(Citation)
            .where(Citation.message_id == message_id)
        )

        result = await session.exec(statement)

        return result.all()

    async def get_by_agent_run(
        self,
        session: AsyncSession,
        agent_run_id,
    ):
        statement = (
            select(Citation)
            .where(Citation.agent_run_id == agent_run_id)
        )

        result = await session.exec(statement)

        return result.all()
