"""
Participant ORM model.
Represents a person who attended one or more meetings.
"""
import uuid
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base
from app.models.meeting import meeting_participants_table


class Participant(Base):
    """A meeting participant (speaker)."""

    __tablename__ = "participants"

    id: Mapped[str] = mapped_column(
        String, primary_key=True, default=lambda: str(uuid.uuid4())
    )
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    email: Mapped[str | None] = mapped_column(String(255), nullable=True)
    avatar_color: Mapped[str] = mapped_column(String(20), default="#7C3AED")

    # Relationships
    meetings: Mapped[list["Meeting"]] = relationship(  # type: ignore[name-defined]  # noqa: F821
        "Meeting",
        secondary=meeting_participants_table,
        back_populates="participants",
    )
