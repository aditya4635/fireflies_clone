"""
Summaries router — handles AI summary retrieval and editing.
"""
import json
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.database import get_db
from app.models.summary import Summary
from app.schemas.summary import SummaryResponse, SummaryUpdate

router = APIRouter(prefix="/meetings/{meeting_id}/summary", tags=["summaries"])


@router.get("", response_model=SummaryResponse)
async def get_summary(
    meeting_id: str,
    db: AsyncSession = Depends(get_db),
):
    stmt = select(Summary).where(Summary.meeting_id == meeting_id)
    result = await db.execute(stmt)
    summary = result.scalar_one_or_none()
    if not summary:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Summary not found")
    return SummaryResponse.model_validate(summary)


@router.patch("", response_model=SummaryResponse)
async def update_summary(
    meeting_id: str,
    data: SummaryUpdate,
    db: AsyncSession = Depends(get_db),
):
    stmt = select(Summary).where(Summary.meeting_id == meeting_id)
    result = await db.execute(stmt)
    summary = result.scalar_one_or_none()
    if not summary:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Summary not found")

    if data.overview is not None:
        summary.overview = data.overview
    if data.key_topics is not None:
        summary.key_topics = json.dumps(data.key_topics)
    if data.chapters is not None:
        summary.chapters = json.dumps([c.model_dump() for c in data.chapters])
    if data.sentiment is not None:
        summary.sentiment = data.sentiment

    await db.commit()
    await db.refresh(summary)
    return SummaryResponse.model_validate(summary)
