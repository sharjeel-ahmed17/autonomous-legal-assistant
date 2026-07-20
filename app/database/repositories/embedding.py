from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.database.models.embedding import Embedding
from app.database.repositories.base import BaseRepository


class EmbeddingRepository(BaseRepository[Embedding]):
    def __init__(self):
        super().__init__(Embedding)

    async def get_by_chunk(
        self,
        session: AsyncSession,
        document_chunk_id,
    ):
        statement = (
            select(Embedding)
            .where(Embedding.document_chunk_id == document_chunk_id)
        )

        result = await session.exec(statement)

        return result.all()
