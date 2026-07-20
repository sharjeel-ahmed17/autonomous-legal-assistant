from uuid import UUID

from pydantic import BaseModel

from app.database.schemas.common import TimestampSchema, UUIDBaseSchema


class DocumentChunkCreate(BaseModel):
    document_id: UUID
    chunk_index: int
    content: str
    page_number: int | None = None
    token_count: int | None = None
    metadata_json: str | None = None


class DocumentChunkRead(UUIDBaseSchema, TimestampSchema):
    document_id: UUID
    chunk_index: int
    content: str
    page_number: int | None
    token_count: int | None
    metadata_json: str | None
    embedding_id: str | None
