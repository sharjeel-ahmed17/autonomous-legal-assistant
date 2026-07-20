from uuid import UUID

from pydantic import BaseModel

from app.database.schemas.common import TimestampSchema, UUIDBaseSchema


class AuditLogCreate(BaseModel):
    user_id: UUID | None = None
    action: str
    resource_type: str
    resource_id: UUID | None = None
    details: str | None = None
    ip_address: str | None = None


class AuditLogRead(UUIDBaseSchema, TimestampSchema):
    user_id: UUID | None
    action: str
    resource_type: str
    resource_id: UUID | None
    details: str | None
    ip_address: str | None
