"""
Transcripts router — handles transcript retrieval, search, and upload.
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, Query, UploadFile, File, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.schemas.transcript import TranscriptLineResponse, TranscriptUploadResponse
from app.services.transcript_service import TranscriptService

router = APIRouter(prefix="/meetings/{meeting_id}/transcript", tags=["transcripts"])


@router.get("", response_model=List[TranscriptLineResponse])
async def get_transcript(
    meeting_id: str,
    db: AsyncSession = Depends(get_db),
):
    service = TranscriptService(db)
    lines = await service.get_transcript(meeting_id)
    return [TranscriptLineResponse.model_validate(l) for l in lines]


@router.get("/search", response_model=List[TranscriptLineResponse])
async def search_transcript(
    meeting_id: str,
    q: str = Query(..., min_length=1),
    db: AsyncSession = Depends(get_db),
):
    service = TranscriptService(db)
    lines = await service.search_transcript(meeting_id, q)
    return [TranscriptLineResponse.model_validate(l) for l in lines]


@router.post("/upload", response_model=TranscriptUploadResponse)
async def upload_transcript(
    meeting_id: str,
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
):
    service = TranscriptService(db)
    content = await file.read()
    text = content.decode("utf-8", errors="replace")

    filename = file.filename or ""
    if filename.endswith(".vtt"):
        count = await service.import_vtt(meeting_id, text)
    else:
        count = await service.import_transcript_text(meeting_id, text)

    return TranscriptUploadResponse(lines_imported=count, message=f"Imported {count} transcript lines")


@router.post("/paste", response_model=TranscriptUploadResponse)
async def paste_transcript(
    meeting_id: str,
    payload: dict,
    db: AsyncSession = Depends(get_db),
):
    """Accept raw transcript text pasted by the user."""
    text = payload.get("text", "")
    if not text:
        raise HTTPException(status_code=400, detail="No transcript text provided")
    service = TranscriptService(db)
    count = await service.import_transcript_text(meeting_id, text)
    return TranscriptUploadResponse(lines_imported=count, message=f"Imported {count} transcript lines")
