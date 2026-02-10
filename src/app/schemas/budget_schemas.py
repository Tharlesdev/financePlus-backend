from pydantic import BaseModel, UUID4, Field, validator
from datetime import datetime

class BudgetCreate(BaseModel):
    category_id: UUID4
    amount: float = Field(..., gt=0)
    month: str = Field(..., pattern=r"^\d{4}-\d{2}$") # YYYY-MM

class BudgetResponse(BaseModel):
    id: UUID4
    user_id: UUID4
    category_id: UUID4
    amount: float
    month: str
    created_at: datetime
    
    # Para status
    spent: float = 0.0
    remaining: float = 0.0
    percentage: float = 0.0

    class Config:
        from_attributes = True
