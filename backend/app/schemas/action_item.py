"""Pydantic schemas for ActionItem resources."""
from __future__ import annotations
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict


class ActionItemCreate(BaseModel):
    text: str
    assignee: Optional[str] = None
    due_date: Optional[datetime] = None
    priority: str = "medium"


class ActionItemUpdate(BaseModel):
    text: Optional[str] = None
    assignee: Optional[str] = None
    due_date: Optional[datetime] = None
    completed: Optional[bool] = None
    priority: Optional[str] = None


class ActionItemResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    meeting_id: str
    assignee: Optional[str]
    text: str
    due_date: Optional[datetime]
    completed: bool
    priority: str
    created_at: datetime
    updated_at: datetime
