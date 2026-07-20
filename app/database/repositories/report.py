from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.database.models.report import Report
from app.database.repositories.base import BaseRepository


class ReportRepository(BaseRepository[Report]):
    def __init__(self):
        super().__init__(Report)

    async def get_by_user(
        self,
        session: AsyncSession,
        user_id,
    ):
        statement = (
            select(Report)
            .where(Report.user_id == user_id)
        )

        result = await session.exec(statement)

        return result.all()

    async def get_by_agent_run(
        self,
        session: AsyncSession,
        agent_run_id,
    ):
        statement = (
            select(Report)
            .where(Report.agent_run_id == agent_run_id)
        )

        result = await session.exec(statement)

        return result.all()
