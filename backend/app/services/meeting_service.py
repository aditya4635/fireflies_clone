"""
Meeting service — business logic for meeting CRUD operations.
Orchestrates repositories and handles participant management.
"""
import uuid
from typing import List, Optional, Tuple
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException, status

from app.models.meeting import Meeting, meeting_participants_table
from app.models.participant import Participant
from app.repositories.meeting_repo import MeetingRepository
from app.schemas.meeting import MeetingCreate, MeetingUpdate, MeetingResponse, MeetingListResponse


class MeetingService:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db
        self.repo = MeetingRepository(db)

    async def list_meetings(
        self, search: Optional[str], topic: Optional[str], page: int, page_size: int
    ) -> MeetingListResponse:
        items, total = await self.repo.list_with_filters(search=search, topic=topic, page=page, page_size=page_size)
        return MeetingListResponse(
            items=[MeetingResponse.model_validate(m) for m in items],
            total=total,
            page=page,
            page_size=page_size,
        )

    async def get_meeting(self, meeting_id: str) -> Meeting:
        meeting = await self.repo.get_by_id_full(meeting_id)
        if not meeting:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Meeting not found")
        return meeting

    async def create_meeting(self, data: MeetingCreate) -> Meeting:
        meeting = Meeting(
            id=str(uuid.uuid4()),
            workspace_id="ws_default",
            title=data.title,
            date=data.date,
            duration=data.duration,
        )
        self.db.add(meeting)
        await self.db.flush()

        # Create participants and link them
        for p_data in data.participants:
            participant = Participant(
                id=str(uuid.uuid4()),
                name=p_data.name,
                email=p_data.email,
                avatar_color=p_data.avatar_color or "#7C3AED",
            )
            self.db.add(participant)
            await self.db.flush()

            link_stmt = meeting_participants_table.insert().values(
                meeting_id=meeting.id, participant_id=participant.id
            )
            await self.db.execute(link_stmt)

        await self.db.commit()
        return await self.repo.get_by_id_full(meeting.id)

    async def update_meeting(self, meeting_id: str, data: MeetingUpdate) -> Meeting:
        meeting = await self.get_meeting(meeting_id)
        update_data = data.model_dump(exclude_unset=True, exclude={"participants"})
        await self.repo.update(meeting, update_data)

        if data.participants is not None:
            # Remove all existing participant links
            del_stmt = meeting_participants_table.delete().where(
                meeting_participants_table.c.meeting_id == meeting_id
            )
            await self.db.execute(del_stmt)

            # Add new ones
            for p_data in data.participants:
                participant = Participant(
                    id=str(uuid.uuid4()),
                    name=p_data.name,
                    email=p_data.email,
                    avatar_color=p_data.avatar_color or "#7C3AED",
                )
                self.db.add(participant)
                await self.db.flush()
                link_stmt = meeting_participants_table.insert().values(
                    meeting_id=meeting_id, participant_id=participant.id
                )
                await self.db.execute(link_stmt)

        await self.db.commit()
        return await self.repo.get_by_id_full(meeting_id)

    async def delete_meeting(self, meeting_id: str) -> None:
        meeting = await self.get_meeting(meeting_id)
        await self.repo.delete(meeting)
        await self.db.commit()
