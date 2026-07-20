from __future__ import annotations

from uuid import UUID

from sqlmodel import Field, Relationship

from app.database.models.base import BaseModel


class Feedback(BaseModel, table=True):
    __tablename__ = "feedback"

    user_id: UUID = Field(foreign_key="users.id")
    message_id: UUID | None = Field(default=None, foreign_key="messages.id")
    agent_run_id: UUID | None = Field(default=None, foreign_key="agent_runs.id")

    rating: int
    comment: str | None = None
    category: str | None = None
    metadata_json: str | None = None

    user: "User" = Relationship(back_populates="feedback")
    message: "Message" | None = Relationship(back_populates="feedback")
    agent_run: "AgentRun" | None = Relationship(back_populates="feedback")
