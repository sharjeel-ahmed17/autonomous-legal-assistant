from uuid import UUID

from pydantic import BaseModel

from app.database.schemas.common import TimestampSchema, UUIDBaseSchema


class EmbeddingCreate(BaseModel):
    document_chunk_id: UUID
    model_name: str
    vector_store_id: str
    dimensions: int
    metadata_json: str | None = None


class EmbeddingRead(UUIDBaseSchema, TimestampSchema):
    document_chunk_id: UUID
    model_name: str
    vector_store_id: str
    dimensions: int
    metadata_json: str | None
