"""Pydantic schemas for Summary resources."""
from __future__ import annotations
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, ConfigDict, field_validator
import json


class ChapterSchema(BaseModel):
    title: str
    start_time: float
    summary: str


class SummaryResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    meeting_id: str
    overview: str
    key_topics: List[str]
    chapters: List[ChapterSchema]
    sentiment: str
    created_at: datetime
    updated_at: datetime

    @field_validator("key_topics", mode="before")
    @classmethod
    def parse_key_topics(cls, v):
        if isinstance(v, str):
            return json.loads(v)
        return v

    @field_validator("chapters", mode="before")
    @classmethod
    def parse_chapters(cls, v):
        if isinstance(v, str):
            return json.loads(v)
        return v


class SummaryUpdate(BaseModel):
    overview: Optional[str] = None
    key_topics: Optional[List[str]] = None
    chapters: Optional[List[ChapterSchema]] = None
    sentiment: Optional[str] = None
