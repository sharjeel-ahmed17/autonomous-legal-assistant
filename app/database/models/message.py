from __future__ import annotations

from uuid import UUID

from sqlmodel import Field, Relationship

from app.database.models.base import BaseModel


class Message(BaseModel, table=True):
    __tablename__ = "messages"

    role: str
    content: str
    token_count: int | None = None
    metadata_json: str | None = None

    conversation_id: UUID = Field(foreign_key="conversations.id")

    conversation: "Conversation" = Relationship(back_populates="messages")
    citations: list["Citation"] = Relationship(back_populates="message")
    feedback: list["Feedback"] = Relationship(back_populates="message")
