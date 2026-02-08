# pylint: disable=W0223
# pylint: disable=R0901

import uuid
from datetime import datetime, timezone
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.app.externals.models.base import Base

if TYPE_CHECKING:
    from src.app.externals.models.transaction import Transaction


def utc_now():
    return datetime.now(timezone.utc).replace(tzinfo=None)


class Category(Base):
    """Categoria de transações (ex: Alimentação, Transporte, etc)."""

    __tablename__ = "categories"

    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    name: Mapped[str] = mapped_column(String, nullable=False)

    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=utc_now
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=True, onupdate=utc_now
    )

    name: Mapped[str] = mapped_column(String, nullable=False)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"), nullable=False)

    user = relationship("User", back_populates="categories")
    transactions: Mapped[list["Transaction"]] = relationship(
        "Transaction", back_populates="category", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"User (id={str(self.id)}, name={self.name}"

    @property
    def as_dict(self):
        return {
            "id": str(self.id),
            "name": self.name,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
