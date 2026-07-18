"""
Meetings router — handles all /api/v1/meetings endpoints.
"""
from typing import Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.schemas.meeting import MeetingCreate, MeetingUpdate, MeetingResponse, MeetingListResponse
from app.services.meeting_service import MeetingService

router = APIRouter(prefix="/meetings", tags=["meetings"])


@router.get("", response_model=MeetingListResponse)
async def list_meetings(
    search: Optional[str] = Query(None, description="Search by title or participant"),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    service = MeetingService(db)
    return await service.list_meetings(search=search, page=page, page_size=page_size)


@router.post("", response_model=MeetingResponse, status_code=201)
async def create_meeting(
    data: MeetingCreate,
    db: AsyncSession = Depends(get_db),
):
    service = MeetingService(db)
    meeting = await service.create_meeting(data)
    return MeetingResponse.model_validate(meeting)


@router.get("/{meeting_id}", response_model=MeetingResponse)
async def get_meeting(
    meeting_id: str,
    db: AsyncSession = Depends(get_db),
):
    service = MeetingService(db)
    meeting = await service.get_meeting(meeting_id)
    return MeetingResponse.model_validate(meeting)


@router.patch("/{meeting_id}", response_model=MeetingResponse)
async def update_meeting(
    meeting_id: str,
    data: MeetingUpdate,
    db: AsyncSession = Depends(get_db),
):
    service = MeetingService(db)
    meeting = await service.update_meeting(meeting_id, data)
    return MeetingResponse.model_validate(meeting)


@router.delete("/{meeting_id}", status_code=204)
async def delete_meeting(
    meeting_id: str,
    db: AsyncSession = Depends(get_db),
):
    service = MeetingService(db)
    await service.delete_meeting(meeting_id)
