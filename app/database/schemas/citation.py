from uuid import UUID

from pydantic import BaseModel, Field

from app.database.schemas.common import TimestampSchema, UUIDBaseSchema


class CitationCreate(BaseModel):
    document_id: UUID
    message_id: UUID | None = None
    agent_run_id: UUID | None = None
    citation_text: str
    source_page: int | None = None
    relevance_score: float | None = Field(default=None, ge=0.0, le=1.0)
    metadata_json: str | None = None


class CitationRead(UUIDBaseSchema, TimestampSchema):
    document_id: UUID
    message_id: UUID | None
    agent_run_id: UUID | None
    citation_text: str
    source_page: int | None
    relevance_score: float | None
    metadata_json: str | None
