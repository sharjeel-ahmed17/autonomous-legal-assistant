from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.database.models.document_chunks import DocumentChunk
from app.database.repositories.base import BaseRepository


class DocumentChunkRepository(BaseRepository[DocumentChunk]):
    def __init__(self):
        super().__init__(DocumentChunk)

    async def get_by_document(
        self,
        session: AsyncSession,
        document_id,
    ):
        statement = (
            select(DocumentChunk)
            .where(DocumentChunk.document_id == document_id)
        )

        result = await session.exec(statement)

        return result.all()
