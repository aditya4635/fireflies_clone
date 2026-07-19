"""
Shared SQLAlchemy mixins for enterprise features.
"""
from datetime import datetime
from typing import Optional
from sqlalchemy import DateTime, String, func
from sqlalchemy.orm import Mapped, mapped_column


class AuditableBase:
    """
    Mixin that adds auditing and soft-delete columns to any SQLAlchemy model.
    """
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())
    deleted_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    created_by: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)
    updated_by: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)

    @property
    def is_deleted(self) -> bool:
        return self.deleted_at is not None
