"""
Summary ORM model.
Stores AI-generated summary data for a meeting (1:1 with Meeting).
"""
import uuid
import enum
from datetime import datetime
from sqlalchemy import String, Text, ForeignKey, DateTime, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base
from app.models.base import AuditableBase
from app.models.topic import summary_topics_table


class SentimentEnum(str, enum.Enum):
    POSITIVE = "positive"
    NEUTRAL = "neutral"
    NEGATIVE = "negative"


class Summary(Base, AuditableBase):
    """AI-generated meeting summary (one per meeting)."""

    __tablename__ = "summaries"

    id: Mapped[str] = mapped_column(
        String, primary_key=True, default=lambda: str(uuid.uuid4())
    )
    workspace_id: Mapped[str] = mapped_column(
        String, ForeignKey("workspaces.id", ondelete="CASCADE"), nullable=False, index=True
    )
    meeting_id: Mapped[str] = mapped_column(
        String, ForeignKey("meetings.id", ondelete="CASCADE"), unique=True, nullable=False
    )
    overview: Mapped[str] = mapped_column(Text, nullable=False)
    sentiment: Mapped[SentimentEnum] = mapped_column(
        Enum(SentimentEnum, name="sentiment_enum"), default=SentimentEnum.NEUTRAL
    )

    # Relationships
    workspace: Mapped["Workspace"] = relationship(  # type: ignore[name-defined]  # noqa: F821
        "Workspace"
    )
    meeting: Mapped["Meeting"] = relationship(  # type: ignore[name-defined]  # noqa: F821
        "Meeting", back_populates="summary"
    )
    chapters: Mapped[list["Chapter"]] = relationship(  # type: ignore[name-defined]  # noqa: F821
        "Chapter",
        back_populates="summary",
        cascade="all, delete-orphan",
        order_by="Chapter.start_time",
    )
    topics: Mapped[list["Topic"]] = relationship(  # type: ignore[name-defined]  # noqa: F821
        "Topic",
        secondary=summary_topics_table,
        back_populates="summaries",
        lazy="selectin",
    )
