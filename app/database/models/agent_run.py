from datetime import datetime
from decimal import Decimal
from typing import Optional
from uuid import UUID

from sqlmodel import Field, Relationship

from app.database.models.base import BaseModel


class AgentRun(BaseModel, table=True):
    __tablename__ = "agent_runs"

    user_id: UUID = Field(foreign_key="users.id")
    conversation_id: UUID | None = Field(default=None, foreign_key="conversations.id")

    agent_type: str
    status: str = "pending"

    input_data: str
    output_data: str | None = None
    error_message: str | None = None
    metadata_json: str | None = None

    started_at: datetime | None = None
    completed_at: datetime | None = None
    duration_ms: int | None = None

    user: "User" = Relationship(back_populates="agent_runs")
    conversation: Optional["Conversation"] = Relationship(back_populates="agent_runs")
    citations: list["Citation"] = Relationship(back_populates="agent_run")
    feedback: list["Feedback"] = Relationship(back_populates="agent_run")
    reports: list["Report"] = Relationship(back_populates="agent_run")
