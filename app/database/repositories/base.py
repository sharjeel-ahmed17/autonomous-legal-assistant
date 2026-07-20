from __future__ import annotations

from typing import Any, Generic, TypeVar

from sqlmodel import SQLModel, select
from sqlmodel.ext.asyncio.session import AsyncSession

ModelType = TypeVar("ModelType", bound=SQLModel)


class BaseRepository(Generic[ModelType]):
    def __init__(self, model: type[ModelType]):
        self.model = model

    async def create(
        self,
        session: AsyncSession,
        obj: ModelType,
    ) -> ModelType:
        session.add(obj)
        await session.commit()
        await session.refresh(obj)
        return obj

    async def get_by_id(
        self,
        session: AsyncSession,
        obj_id: Any,
    ) -> ModelType | None:
        return await session.get(self.model, obj_id)

    async def get_all(
        self,
        session: AsyncSession,
    ) -> list[ModelType]:
        statement = select(self.model)
        result = await session.exec(statement)
        return result.all()

    async def delete(
        self,
        session: AsyncSession,
        obj: ModelType,
    ) -> None:
        await session.delete(obj)
        await session.commit()

    async def update(
        self,
        session: AsyncSession,
        obj: ModelType,
    ) -> ModelType:
        session.add(obj)
        await session.commit()
        await session.refresh(obj)
        return obj