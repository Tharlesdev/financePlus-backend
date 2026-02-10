import uuid
from datetime import datetime
from sqlalchemy import String, Float, ForeignKey, DateTime, Boolean, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.app.externals.models.base import Base

class RecurringTransaction(Base):
    __tablename__ = "recurring_transactions"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"), nullable=False)
    category_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("categories.id"), nullable=False)
    
    description: Mapped[str] = mapped_column(String, nullable=False)
    amount: Mapped[float] = mapped_column(Float, nullable=False)
    type: Mapped[str] = mapped_column(String, nullable=False)  # income, expense
    
    frequency: Mapped[str] = mapped_column(String, nullable=False) # monthly, weekly, yearly
    start_date: Mapped[datetime] = mapped_column(Date, nullable=False)
    next_run: Mapped[datetime] = mapped_column(Date, nullable=False)
    active: Mapped[bool] = mapped_column(Boolean, default=True)
    
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relacionamentos
    user = relationship("User")
    category = relationship("Category")
