"""
Chapter ORM model.
Represents a section of a meeting with a summary and start time.
"""
import uuid
from sqlalchemy import String, Float, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base
from app.models.base import AuditableBase


class Chapter(Base, AuditableBase):
    """A distinct segment or chapter of a meeting."""

    __tablename__ = "chapters"

    id: Mapped[str] = mapped_column(
        String, primary_key=True, default=lambda: str(uuid.uuid4())
    )
    workspace_id: Mapped[str] = mapped_column(
        String, ForeignKey("workspaces.id", ondelete="CASCADE"), nullable=False, index=True
    )
    summary_id: Mapped[str] = mapped_column(
        String, ForeignKey("summaries.id", ondelete="CASCADE"), nullable=False, index=True
    )
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    summary_text: Mapped[str] = mapped_column(Text, nullable=False)
    start_time: Mapped[float] = mapped_column(Float, nullable=False)

    # Relationships
    workspace: Mapped["Workspace"] = relationship(  # type: ignore[name-defined]  # noqa: F821
        "Workspace"
    )
    summary: Mapped["Summary"] = relationship(  # type: ignore[name-defined]  # noqa: F821
        "Summary", back_populates="chapters"
    )
