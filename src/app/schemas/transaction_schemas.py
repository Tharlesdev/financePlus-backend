from pydantic import BaseModel, ConfigDict
from datetime import datetime
from uuid import UUID

class TransactionBase(BaseModel):
    type: str
    amount: float
    description: str | None = None
    category_id: UUID

class TransactionCreate(TransactionBase):
    pass

class TransactionResponse(TransactionBase):
    id: UUID
    created_at: datetime
    updated_at: datetime | None = None
    user_id: UUID
    
    model_config = ConfigDict(from_attributes=True)
