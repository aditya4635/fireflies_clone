"""
TranscriptLine ORM model.
Represents a single time-aligned utterance in a meeting transcript.
"""
import uuid
from datetime import datetime
from sqlalchemy import String, Float, Integer, Text, ForeignKey, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base


class TranscriptLine(Base):
    """A single speaker utterance with start/end timestamps."""

    __tablename__ = "transcript_lines"

    id: Mapped[str] = mapped_column(
        String, primary_key=True, default=lambda: str(uuid.uuid4())
    )
    meeting_id: Mapped[str] = mapped_column(
        String, ForeignKey("meetings.id", ondelete="CASCADE"), nullable=False, index=True
    )
    participant_id: Mapped[str | None] = mapped_column(
        String, ForeignKey("participants.id"), nullable=True
    )
    speaker_name: Mapped[str] = mapped_column(String(200), nullable=False)
    start_time: Mapped[float] = mapped_column(Float, nullable=False)   # seconds
    end_time: Mapped[float] = mapped_column(Float, nullable=False)     # seconds
    text: Mapped[str] = mapped_column(Text, nullable=False)
    sequence_number: Mapped[int] = mapped_column(Integer, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now()
    )

    # Relationships
    meeting: Mapped["Meeting"] = relationship(  # type: ignore[name-defined]  # noqa: F821
        "Meeting", back_populates="transcript_lines"
    )
