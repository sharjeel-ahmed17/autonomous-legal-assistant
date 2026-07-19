from uuid import UUID

from sqlmodel import Field, Relationship

from app.database.models.base import BaseModel
from app.database.models.role import UserRoleLink


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
    api_keys: list["ApiKey"] = Relationship(back_populates="user")
    feedback: list["Feedback"] = Relationship(back_populates="user")
    notifications: list["Notification"] = Relationship(back_populates="user")
    refresh_tokens: list["RefreshToken"] = Relationship(back_populates="user")
    reports: list["Report"] = Relationship(back_populates="user")
    roles: list["Role"] = Relationship(back_populates="users", link_model=UserRoleLink)
