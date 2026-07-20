from pydantic import BaseModel, Field

from app.database.schemas.common import TimestampSchema, UUIDBaseSchema


class WorkflowCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    description: str | None = None
    version: str = "1.0.0"
    config: str | None = None
    metadata_json: str | None = None


class WorkflowUpdate(BaseModel):
    description: str | None = None
    version: str | None = None
    config: str | None = None
    is_active: bool | None = None
    metadata_json: str | None = None


class WorkflowRead(UUIDBaseSchema, TimestampSchema):
    name: str
    description: str | None
    version: str
    config: str | None
    is_active: bool
    metadata_json: str | None
