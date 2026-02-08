# pylint: disable=W0223
# pylint: disable=R0901

import uuid
from datetime import datetime, timezone

from sqlalchemy import DECIMAL, DateTime, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.app.externals.models.base import Base


def utc_now():
    return datetime.now(timezone.utc).replace(tzinfo=None)


class Transaction(Base):
    __tablename__ = "transaction"

    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    type: Mapped[str] = mapped_column(String, nullable=False)

    amount: Mapped[float] = mapped_column(DECIMAL, nullable=False)

    description: Mapped[str | None] = mapped_column(String, nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=utc_now
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=True, onupdate=utc_now
    )

    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"), nullable=False)
    category_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("categories.id"), nullable=False
    )

    user = relationship("User", back_populates="transactions")
    category = relationship("Category", back_populates="transactions")

    def __repr__(self):
        return f"User (id={str(self.id)}, type={self.type}, amount={self.amount})"

    @property
    def as_dict(self):
        return {
            "id": str(self.id),
            "type": self.type,
            "amount": self.amount,
            "created_at": self.created_at.isoformat(),
            "description": self.description,
        }
