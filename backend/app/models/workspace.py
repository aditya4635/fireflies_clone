"""
Workspace ORM model.
Represents a tenant or organization.
"""
import uuid
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base
from app.models.base import AuditableBase


class Workspace(Base, AuditableBase):
    """A tenant/organization that owns meetings and members."""

    __tablename__ = "workspaces"

    id: Mapped[str] = mapped_column(
        String, primary_key=True, default=lambda: str(uuid.uuid4())
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    domain: Mapped[str | None] = mapped_column(String(255), nullable=True, unique=True)

    # Relationships
    meetings: Mapped[list["Meeting"]] = relationship(  # type: ignore[name-defined]  # noqa: F821
        "Meeting",
        back_populates="workspace",
        cascade="all, delete-orphan",
    )
