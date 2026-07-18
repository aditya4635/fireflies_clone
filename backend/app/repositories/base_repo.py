"""
Base repository implementing generic async CRUD operations.
All entity-specific repositories inherit from this class (DRY principle).
"""
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

    async def get_by_id(self, entity_id: str) -> Optional[ModelT]:
        result = await self.db.get(self.model, entity_id)
        return result

    async def get_all(self, offset: int = 0, limit: int = 50) -> List[ModelT]:
        stmt = select(self.model).offset(offset).limit(limit)
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def count(self) -> int:
        stmt = select(func.count()).select_from(self.model)
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
        await self.db.delete(obj)
        await self.db.flush()
