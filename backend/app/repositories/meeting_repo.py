"""
Meeting-specific repository.
Handles search, filtering, and sorting on top of base CRUD.
"""
from typing import List, Optional, Tuple
from sqlalchemy import select, func, or_
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.meeting import Meeting
from app.repositories.base_repo import BaseRepository


class MeetingRepository(BaseRepository[Meeting]):
    def __init__(self, db: AsyncSession) -> None:
        super().__init__(Meeting, db)

    async def get_by_id_full(self, meeting_id: str) -> Optional[Meeting]:
        """Fetch meeting with all relationships eagerly loaded."""
        stmt = (
            select(Meeting)
            .where(Meeting.id == meeting_id)
            .options(
                selectinload(Meeting.participants),
                selectinload(Meeting.summary),
                selectinload(Meeting.action_items),
            )
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def list_with_filters(
        self,
        search: Optional[str] = None,
        topic: Optional[str] = None,
        page: int = 1,
        page_size: int = 20,
    ) -> Tuple[List[Meeting], int]:
        """Return paginated meetings filtered by optional search query and topic."""
        base_query = select(Meeting).options(selectinload(Meeting.participants))

        if search:
            base_query = base_query.where(
                or_(
                    Meeting.title.ilike(f"%{search}%"),
                )
            )

        if topic:
            from app.models.summary import Summary
            base_query = base_query.join(Meeting.summary).where(
                Summary.key_topics.ilike(f'%"{topic}"%')
            )

        # Total count
        count_stmt = select(func.count()).select_from(base_query.subquery())
        total = (await self.db.execute(count_stmt)).scalar_one()

        # Paginated results
        stmt = (
            base_query
            .order_by(Meeting.date.desc())
            .offset((page - 1) * page_size)
            .limit(page_size)
        )
        result = await self.db.execute(stmt)
        return list(result.scalars().all()), total
