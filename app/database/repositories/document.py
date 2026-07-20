from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.database.models.document import Document
from app.database.repositories.base import BaseRepository


class DocumentRepository(BaseRepository[Document]):
    def __init__(self):
        super().__init__(Document)

    async def get_by_owner(
        self,
        session: AsyncSession,
        owner_id,
    ) -> list[Document]:
        statement = (
            select(Document)
            .where(Document.owner_id == owner_id)
        )

        result = await session.exec(statement)

        return result.all()