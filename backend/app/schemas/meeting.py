"""
Pydantic schemas for Meeting and Participant resources.
Separates API contract from ORM models (Dependency Inversion Principle).
"""
from __future__ import annotations
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, ConfigDict, field_validator, model_validator


# ---------------------------------------------------------------------------
# Participant
# ---------------------------------------------------------------------------

class ParticipantCreate(BaseModel):
    name: str
    email: Optional[str] = None
    avatar_color: Optional[str] = "#7C3AED"


class ParticipantResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    name: str
    email: Optional[str]
    avatar_color: str


# ---------------------------------------------------------------------------
# Meeting
# ---------------------------------------------------------------------------

class MeetingCreate(BaseModel):
    title: str
    date: datetime
    duration: int  # seconds
    participants: List[ParticipantCreate] = []
    transcript_text: Optional[str] = None  # raw pasted transcript


class MeetingUpdate(BaseModel):
    title: Optional[str] = None
    date: Optional[datetime] = None
    duration: Optional[int] = None
    participants: Optional[List[ParticipantCreate]] = None


class MeetingResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    title: str
    date: datetime
    duration: int
    bot_name: str
    status: str
    source: str
    created_at: datetime
    updated_at: datetime
    participants: List[ParticipantResponse] = []

    @field_validator("date", "created_at", "updated_at", mode="before")
    @classmethod
    def ensure_datetime(cls, v):
        return v

    @model_validator(mode="before")
    @classmethod
    def handle_enums(cls, data):
        if hasattr(data, "status") and hasattr(data.status, "value"):
            data.status = data.status.value
        return data


class MeetingListResponse(BaseModel):
    """Paginated list of meetings."""

    items: List[MeetingResponse]
    total: int
    page: int
    page_size: int
