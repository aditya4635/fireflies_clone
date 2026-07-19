"""
ActionItem ORM model.
Represents a task extracted from a meeting, with completion tracking.
"""
import uuid
import enum
from datetime import datetime
from sqlalchemy import String, Text, Boolean, ForeignKey, DateTime, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base
from app.models.base import AuditableBase


class ActionItemPriority(str, enum.Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class ActionItem(Base, AuditableBase):
    """A task or follow-up extracted from meeting content."""

    __tablename__ = "action_items"

    id: Mapped[str] = mapped_column(
        String, primary_key=True, default=lambda: str(uuid.uuid4())
    )
    workspace_id: Mapped[str] = mapped_column(
        String, ForeignKey("workspaces.id", ondelete="CASCADE"), nullable=False, index=True
    )
    meeting_id: Mapped[str] = mapped_column(
        String, ForeignKey("meetings.id", ondelete="CASCADE"), nullable=False, index=True
    )
    assignee: Mapped[str | None] = mapped_column(String(200), nullable=True)
    text: Mapped[str] = mapped_column(Text, nullable=False)
    due_date: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    completed: Mapped[bool] = mapped_column(Boolean, default=False)
    priority: Mapped[ActionItemPriority] = mapped_column(
        Enum(ActionItemPriority, name="action_priority_enum"), default=ActionItemPriority.MEDIUM
    )

    # Relationships
    workspace: Mapped["Workspace"] = relationship(  # type: ignore[name-defined]  # noqa: F821
        "Workspace"
    )
    meeting: Mapped["Meeting"] = relationship(  # type: ignore[name-defined]  # noqa: F821
        "Meeting", back_populates="action_items"
    )
