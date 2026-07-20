from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from app.database.schemas.common import TimestampSchema, UUIDBaseSchema


class AgentRunCreate(BaseModel):
    conversation_id: UUID | None = None
    agent_type: str
    input_data: str
    metadata_json: str | None = None


class AgentRunUpdate(BaseModel):
    status: str | None = None
    output_data: str | None = None
    error_message: str | None = None
    metadata_json: str | None = None
    started_at: datetime | None = None
    completed_at: datetime | None = None
    duration_ms: int | None = None


class AgentRunRead(UUIDBaseSchema, TimestampSchema):
    user_id: UUID
    conversation_id: UUID | None
    agent_type: str
    status: str
    input_data: str
    output_data: str | None
    error_message: str | None
    metadata_json: str | None
    started_at: datetime | None
    completed_at: datetime | None
    duration_ms: int | None
