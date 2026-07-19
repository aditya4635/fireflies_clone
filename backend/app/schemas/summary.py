"""Pydantic schemas for Summary resources."""
from __future__ import annotations
from datetime import datetime
from typing import List, Optional, Any
from pydantic import BaseModel, ConfigDict, model_validator


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

    @model_validator(mode="before")
    @classmethod
    def map_orm_relations(cls, data: Any) -> Any:
        # If it's an ORM object, extract relationships to match the old JSON shape
        if hasattr(data, "topics"):
            data.key_topics = [t.name for t in data.topics] if data.topics else []
        if hasattr(data, "chapters") and hasattr(data.chapters, "__iter__"):
            # Map ORM 'summary_text' to 'summary' for the frontend API
            data.chapters_mapped = []
            for ch in data.chapters:
                if hasattr(ch, "summary_text"):
                     data.chapters_mapped.append({"title": ch.title, "start_time": ch.start_time, "summary": ch.summary_text})
            data.chapters = data.chapters_mapped
        
        # Handle enum conversion
        if hasattr(data, "sentiment") and hasattr(data.sentiment, "value"):
            data.sentiment = data.sentiment.value

        return data


class SummaryUpdate(BaseModel):
    overview: Optional[str] = None
    key_topics: Optional[List[str]] = None
    chapters: Optional[List[ChapterSchema]] = None
    sentiment: Optional[str] = None
