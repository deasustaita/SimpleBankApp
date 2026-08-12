from pydantic import BaseModel, Field
from datetime import datetime
from models.Transaction import Transaction

class Account(BaseModel):
    account_id: int
    user_id: int
    
    balance: float
    account_type: str

    transactions: list[Transaction] = Field(default_factory=list)

    time_created: datetime = Field(default_factory=datetime.now)