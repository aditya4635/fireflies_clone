"""
Search router — global search across meetings and transcripts.
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_
from pydantic import BaseModel

from app.database import get_db
from app.models.meeting import Meeting
from app.models.transcript import TranscriptLine

router = APIRouter(prefix="/search", tags=["search"])


class SearchResult(BaseModel):
    type: str  # 'meeting' | 'transcript'
    meeting_id: str
    meeting_title: str
    snippet: str
    timestamp: Optional[float] = None


@router.get("", response_model=List[SearchResult])
async def global_search(
    q: str = Query(..., min_length=1),
    db: AsyncSession = Depends(get_db),
):
    results: List[SearchResult] = []

    # Search meetings by title
    meeting_stmt = select(Meeting).where(Meeting.title.ilike(f"%{q}%")).limit(10)
    meeting_res = await db.execute(meeting_stmt)
    for meeting in meeting_res.scalars().all():
        results.append(SearchResult(
            type="meeting",
            meeting_id=meeting.id,
            meeting_title=meeting.title,
            snippet=meeting.title,
        ))

    # Search transcript lines
    transcript_stmt = (
        select(TranscriptLine, Meeting)
        .join(Meeting, Meeting.id == TranscriptLine.meeting_id)
        .where(TranscriptLine.text.ilike(f"%{q}%"))
        .limit(20)
    )
    transcript_res = await db.execute(transcript_stmt)
    for transcript_line, meeting in transcript_res.all():
        results.append(SearchResult(
            type="transcript",
            meeting_id=meeting.id,
            meeting_title=meeting.title,
            snippet=transcript_line.text[:150],
            timestamp=transcript_line.start_time,
        ))

    return results
