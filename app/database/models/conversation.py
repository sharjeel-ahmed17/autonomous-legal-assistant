from uuid import UUID

from sqlmodel import Field, Relationship

from app.database.models.base import BaseModel


class Conversation(BaseModel, table=True):
    __tablename__ = "conversations"

    title: str
    status: str = "active"
    metadata_json: str | None = None

    user_id: UUID = Field(foreign_key="users.id")

    user: "User" = Relationship(back_populates="conversations")
    messages: list["Message"] = Relationship(back_populates="conversation")
    agent_runs: list["AgentRun"] = Relationship(back_populates="conversation")
