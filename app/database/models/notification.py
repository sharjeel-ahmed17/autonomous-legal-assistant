from uuid import UUID

from sqlmodel import Field, Relationship

from app.database.models.base import BaseModel


class Notification(BaseModel, table=True):
    __tablename__ = "notifications"

    user_id: UUID = Field(foreign_key="users.id")
    title: str
    body: str
    type: str = "info"
    is_read: bool = False
    metadata: str | None = None

    user: "User" = Relationship(back_populates="notifications")
