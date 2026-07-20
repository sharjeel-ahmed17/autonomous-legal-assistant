from uuid import UUID

from pydantic import BaseModel, Field

from app.database.schemas.common import TimestampSchema, UUIDBaseSchema


class FeedbackCreate(BaseModel):
    message_id: UUID | None = None
    agent_run_id: UUID | None = None
    rating: int = Field(ge=1, le=5)
    comment: str | None = None
    category: str | None = None
    metadata_json: str | None = None


class FeedbackRead(UUIDBaseSchema, TimestampSchema):
    user_id: UUID
    message_id: UUID | None
    agent_run_id: UUID | None
    rating: int
    comment: str | None
    category: str | None
    metadata_json: str | None
