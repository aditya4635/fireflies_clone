"""
Topic ORM model.
Represents a tag/topic. Includes many-to-many relationship with Summary.
"""
import uuid
from sqlalchemy import String, ForeignKey, Table, Column
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base
from app.models.base import AuditableBase


# Association table for Summary ↔ Topic
summary_topics_table = Table(
    "summary_topics",
    Base.metadata,
    Column("summary_id", String, ForeignKey("summaries.id", ondelete="CASCADE"), primary_key=True),
    Column("topic_id", String, ForeignKey("topics.id", ondelete="CASCADE"), primary_key=True),
)


class Topic(Base, AuditableBase):
    """A topic discussed in one or more meetings."""

    __tablename__ = "topics"

    id: Mapped[str] = mapped_column(
        String, primary_key=True, default=lambda: str(uuid.uuid4())
    )
    workspace_id: Mapped[str] = mapped_column(
        String, ForeignKey("workspaces.id", ondelete="CASCADE"), nullable=False, index=True
    )
    name: Mapped[str] = mapped_column(String(100), nullable=False)

    # Relationships
    workspace: Mapped["Workspace"] = relationship(  # type: ignore[name-defined]  # noqa: F821
        "Workspace"
    )
    summaries: Mapped[list["Summary"]] = relationship(  # type: ignore[name-defined]  # noqa: F821
        "Summary",
        secondary=summary_topics_table,
        back_populates="topics",
    )
