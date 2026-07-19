"""
Base repository implementing generic async CRUD operations.
All entity-specific repositories inherit from this class (DRY principle).
"""
from datetime import datetime
from typing import Any, Dict, Generic, List, Optional, Type, TypeVar
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import Base

ModelT = TypeVar("ModelT", bound=Base)


class BaseRepository(Generic[ModelT]):
    """Generic repository providing common CRUD operations."""

    def __init__(self, model: Type[ModelT], db: AsyncSession) -> None:
        self.model = model
        self.db = db

    def _base_select(self):
        stmt = select(self.model)
        if hasattr(self.model, "deleted_at"):
            stmt = stmt.where(self.model.deleted_at.is_(None))
        return stmt

    async def get_by_id(self, entity_id: str) -> Optional[ModelT]:
        stmt = self._base_select().where(self.model.id == entity_id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_all(self, offset: int = 0, limit: int = 50) -> List[ModelT]:
        stmt = self._base_select().offset(offset).limit(limit)
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def count(self) -> int:
        stmt = select(func.count()).select_from(self.model)
        if hasattr(self.model, "deleted_at"):
            stmt = stmt.where(self.model.deleted_at.is_(None))
        result = await self.db.execute(stmt)
        return result.scalar_one()

    async def create(self, obj: ModelT) -> ModelT:
        self.db.add(obj)
        await self.db.flush()
        await self.db.refresh(obj)
        return obj

    async def update(self, obj: ModelT, data: Dict[str, Any]) -> ModelT:
        for key, value in data.items():
            if hasattr(obj, key) and value is not None:
                setattr(obj, key, value)
        await self.db.flush()
        await self.db.refresh(obj)
        return obj

    async def delete(self, obj: ModelT) -> None:
        if hasattr(obj, "deleted_at"):
            obj.deleted_at = datetime.utcnow()
        else:
            await self.db.delete(obj)
        await self.db.flush()
