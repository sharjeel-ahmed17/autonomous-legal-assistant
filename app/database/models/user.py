from uuid import UUID

from sqlmodel import Field, Relationship, SQLModel

from app.database.models.base import BaseModel


class User(BaseModel, table=True):
    __tablename__ = "users"

    email: str = Field(index=True, unique=True, nullable=False)
    username: str = Field(index=True, unique=True, nullable=False)

    hashed_password: str

    full_name: str | None = None

    is_active: bool = True
    is_superuser: bool = False

    documents: list["Document"] = Relationship(back_populates="owner")
    conversations: list["Conversation"] = Relationship(back_populates="user")
