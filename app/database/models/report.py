from __future__ import annotations

from uuid import UUID

from sqlmodel import Field, Relationship

from app.database.models.base import BaseModel


class Report(BaseModel, table=True):
    __tablename__ = "reports"

    user_id: UUID = Field(foreign_key="users.id")
    agent_run_id: UUID | None = Field(default=None, foreign_key="agent_runs.id")

    title: str
    report_type: str
    content: str
    status: str = "draft"
    metadata_json: str | None = None

    user: "User" = Relationship(back_populates="reports")
    agent_run: "AgentRun" | None = Relationship(back_populates="reports")
