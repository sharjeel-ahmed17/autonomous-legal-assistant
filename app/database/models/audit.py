from uuid import UUID

from sqlmodel import Field

from app.database.models.base import BaseModel


class AuditLog(BaseModel, table=True):
    __tablename__ = "audit_logs"

    user_id: UUID | None = Field(
        default=None,
        foreign_key="users.id",
    )

    action: str

    resource_type: str

    resource_id: UUID | None = None

    details: str | None = None

    ip_address: str | None = None
