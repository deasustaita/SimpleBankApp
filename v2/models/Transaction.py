from pydantic import BaseModel, EmailStr, Field
from datetime import datetime

class Transaction(BaseModel):
    txn_id: int
    account_id: int

    txn_type: str
    amount: float

    created_at: datetime = Field(default_factory=datetime.now)