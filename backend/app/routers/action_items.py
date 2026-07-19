"""
Action Items router — full CRUD for task management.
"""
import uuid
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.database import get_db
from app.models.action_item import ActionItem
from app.schemas.action_item import ActionItemCreate, ActionItemUpdate, ActionItemResponse

router = APIRouter(tags=["action-items"])


@router.get("/meetings/{meeting_id}/action-items", response_model=List[ActionItemResponse])
async def list_action_items(
    meeting_id: str,
    db: AsyncSession = Depends(get_db),
):
    stmt = select(ActionItem).where(
        ActionItem.meeting_id == meeting_id,
        ActionItem.deleted_at.is_(None)
    )
    result = await db.execute(stmt)
    return [ActionItemResponse.model_validate(a) for a in result.scalars().all()]


@router.post("/meetings/{meeting_id}/action-items", response_model=ActionItemResponse, status_code=201)
async def create_action_item(
    meeting_id: str,
    data: ActionItemCreate,
    db: AsyncSession = Depends(get_db),
):
    item = ActionItem(
        id=str(uuid.uuid4()),
        workspace_id="ws_default",
        meeting_id=meeting_id,
        text=data.text,
        assignee=data.assignee,
        due_date=data.due_date,
        priority=data.priority,
    )
    db.add(item)
    await db.commit()
    await db.refresh(item)
    return ActionItemResponse.model_validate(item)


@router.patch("/action-items/{item_id}", response_model=ActionItemResponse)
async def update_action_item(
    item_id: str,
    data: ActionItemUpdate,
    db: AsyncSession = Depends(get_db),
):
    item = await db.get(ActionItem, item_id)
    if not item or item.is_deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Action item not found")

    update_fields = data.model_dump(exclude_unset=True)
    for key, value in update_fields.items():
        setattr(item, key, value)

    await db.commit()
    await db.refresh(item)
    return ActionItemResponse.model_validate(item)


@router.delete("/action-items/{item_id}", status_code=204)
async def delete_action_item(
    item_id: str,
    db: AsyncSession = Depends(get_db),
):
    from datetime import datetime
    item = await db.get(ActionItem, item_id)
    if not item or item.is_deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Action item not found")
    item.deleted_at = datetime.utcnow()
    await db.commit()
