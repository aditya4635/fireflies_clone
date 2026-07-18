"""Pydantic schemas for Transcript resources."""
from __future__ import annotations
from datetime import datetime
from typing import List
from pydantic import BaseModel, ConfigDict


class TranscriptLineResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    meeting_id: str
    participant_id: str | None
    speaker_name: str
    start_time: float
    end_time: float
    text: str
    sequence_number: int
    created_at: datetime


class TranscriptUploadResponse(BaseModel):
    lines_imported: int
    message: str
