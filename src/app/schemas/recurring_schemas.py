from pydantic import BaseModel, UUID4, Field
from datetime import date, datetime
from typing import Literal

class RecurringTransactionCreate(BaseModel):
    category_id: UUID4
    description: str = Field(..., min_length=1)
    amount: float = Field(..., gt=0)
    type: Literal["income", "expense"]
    frequency: Literal["weekly", "monthly", "yearly"]
    start_date: date

class RecurringTransactionResponse(BaseModel):
    id: UUID4
    user_id: UUID4
    category_id: UUID4
    description: str
    amount: float
    type: str
    frequency: str
    start_date: date
    next_run: date
    active: bool
    created_at: datetime

    class Config:
        from_attributes = True
