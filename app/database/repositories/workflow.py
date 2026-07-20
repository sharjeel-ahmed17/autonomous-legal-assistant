from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.database.models.workflow import Workflow
from app.database.repositories.base import BaseRepository


class WorkflowRepository(BaseRepository[Workflow]):
    def __init__(self):
        super().__init__(Workflow)

    async def get_by_name(
        self,
        session: AsyncSession,
        name: str,
    ) -> Workflow | None:
        statement = (
            select(Workflow)
            .where(Workflow.name == name)
        )

        result = await session.exec(statement)

        return result.first()

    async def get_active(
        self,
        session: AsyncSession,
    ):
        statement = (
            select(Workflow)
            .where(Workflow.is_active == True)
        )

        result = await session.exec(statement)

        return result.all()
