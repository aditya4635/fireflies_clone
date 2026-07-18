"""
Summary ORM model.
Stores AI-generated summary data for a meeting (1:1 with Meeting).
key_topics and chapters are stored as JSON strings.
"""
import uuid
from datetime import datetime
from sqlalchemy import String, Text, ForeignKey, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base


class Summary(Base):
    """AI-generated meeting summary (one per meeting)."""

    __tablename__ = "summaries"

    id: Mapped[str] = mapped_column(
        String, primary_key=True, default=lambda: str(uuid.uuid4())
    )
    meeting_id: Mapped[str] = mapped_column(
        String, ForeignKey("meetings.id", ondelete="CASCADE"), unique=True, nullable=False
    )
    overview: Mapped[str] = mapped_column(Text, nullable=False)
    key_topics: Mapped[str] = mapped_column(Text, nullable=False)    # JSON array of strings
    chapters: Mapped[str] = mapped_column(Text, nullable=False)      # JSON array of {title, start_time, summary}
    sentiment: Mapped[str] = mapped_column(String(20), default="neutral")  # positive|neutral|negative
    created_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), onupdate=func.now()
    )

    # Relationships
    meeting: Mapped["Meeting"] = relationship(  # type: ignore[name-defined]  # noqa: F821
        "Meeting", back_populates="summary"
    )
