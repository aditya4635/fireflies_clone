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
        if isinstance(data, dict):
            return data
            
        # If it's an ORM object, extract into a dict
        res = {
            "id": getattr(data, "id", None),
            "meeting_id": getattr(data, "meeting_id", None),
            "overview": getattr(data, "overview", None),
            "created_at": getattr(data, "created_at", None),
            "updated_at": getattr(data, "updated_at", None),
        }
        
        if hasattr(data, "sentiment") and hasattr(data.sentiment, "value"):
            res["sentiment"] = data.sentiment.value
        else:
            res["sentiment"] = getattr(data, "sentiment", None)

        if hasattr(data, "topics"):
            res["key_topics"] = [t.name for t in data.topics] if data.topics else []
        else:
            res["key_topics"] = getattr(data, "key_topics", [])

        if hasattr(data, "chapters") and hasattr(data.chapters, "__iter__"):
            mapped = []
            for ch in data.chapters:
                if hasattr(ch, "summary_text"):
                    mapped.append({"title": ch.title, "start_time": ch.start_time, "summary": ch.summary_text})
                else:
                    mapped.append(ch)
            res["chapters"] = mapped
        else:
            res["chapters"] = getattr(data, "chapters", [])

        return res


class SummaryUpdate(BaseModel):
    overview: Optional[str] = None
    key_topics: Optional[List[str]] = None
    chapters: Optional[List[ChapterSchema]] = None
    sentiment: Optional[str] = None
