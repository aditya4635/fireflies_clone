"""
Meeting ORM model.
Represents a recorded/imported meeting session.
"""
import uuid
import enum
from datetime import datetime
from sqlalchemy import String, Integer, DateTime, ForeignKey, Table, Column, func, Enum, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base
from app.models.base import AuditableBase


# Association table for Meeting ↔ Participant many-to-many
meeting_participants_table = Table(
    "meeting_participants",
    Base.metadata,
    Column("meeting_id", String, ForeignKey("meetings.id", ondelete="CASCADE"), primary_key=True),
    Column("participant_id", String, ForeignKey("participants.id", ondelete="CASCADE"), primary_key=True),
)


class MeetingStatus(str, enum.Enum):
    UPLOADING = "uploading"
    TRANSCRIBING = "transcribing"
    SUMMARIZING = "summarizing"
    COMPLETED = "completed"
    FAILED = "failed"


class Meeting(Base, AuditableBase):
    """Core entity representing a single meeting session."""

    __tablename__ = "meetings"

    id: Mapped[str] = mapped_column(
        String, primary_key=True, default=lambda: str(uuid.uuid4())
    )
    workspace_id: Mapped[str] = mapped_column(
        String, ForeignKey("workspaces.id", ondelete="CASCADE"), nullable=False, index=True
    )
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    duration: Mapped[int] = mapped_column(Integer, nullable=False)  # seconds
    bot_name: Mapped[str] = mapped_column(String(100), default="Fred")
    status: Mapped[MeetingStatus] = mapped_column(
        Enum(MeetingStatus, name="meeting_status_enum"), default=MeetingStatus.COMPLETED
    )
    source: Mapped[str] = mapped_column(String(50), default="upload")

    # Relationships
    workspace: Mapped["Workspace"] = relationship(  # type: ignore[name-defined]  # noqa: F821
        "Workspace", back_populates="meetings"
    )
    transcript_lines: Mapped[list["TranscriptLine"]] = relationship(  # type: ignore[name-defined]  # noqa: F821
        "TranscriptLine",
        back_populates="meeting",
        cascade="all, delete-orphan",
        order_by="TranscriptLine.sequence_number",
    )
    summary: Mapped["Summary"] = relationship(  # type: ignore[name-defined]  # noqa: F821
        "Summary",
        back_populates="meeting",
        cascade="all, delete-orphan",
        uselist=False,
    )
    action_items: Mapped[list["ActionItem"]] = relationship(  # type: ignore[name-defined]  # noqa: F821
        "ActionItem",
        back_populates="meeting",
        cascade="all, delete-orphan",
    )
    participants: Mapped[list["Participant"]] = relationship(  # type: ignore[name-defined]  # noqa: F821
        "Participant",
        secondary=meeting_participants_table,
        back_populates="meetings",
        lazy="selectin",
    )

    __table_args__ = (
        Index("idx_workspace_date", "workspace_id", "date"),
    )
