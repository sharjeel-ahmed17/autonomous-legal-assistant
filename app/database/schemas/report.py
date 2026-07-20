from uuid import UUID

from pydantic import BaseModel

from app.database.schemas.common import TimestampSchema, UUIDBaseSchema


class ReportCreate(BaseModel):
    agent_run_id: UUID | None = None
    title: str
    report_type: str
    content: str
    metadata_json: str | None = None


class ReportUpdate(BaseModel):
    title: str | None = None
    content: str | None = None
    status: str | None = None
    metadata_json: str | None = None


class ReportRead(UUIDBaseSchema, TimestampSchema):
    user_id: UUID
    agent_run_id: UUID | None
    title: str
    report_type: str
    content: str
    status: str
    metadata_json: str | None
