from uuid import UUID

from pydantic import BaseModel, Field

from app.database.schemas.common import TimestampSchema, UUIDBaseSchema


class MessageCreate(BaseModel):
    role: str = Field(pattern=r"^(user|assistant|system|tool)$")
    content: str
    token_count: int | None = None
    metadata_json: str | None = None


class MessageRead(UUIDBaseSchema, TimestampSchema):
    role: str
    content: str
    token_count: int | None
    metadata_json: str | None
    conversation_id: UUID
