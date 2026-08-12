from pydantic import BaseModel, Field
from datetime import datetime

class Account(BaseModel):
    account_id: int
    user_id: int
    
    balance: float
    account_type: str

    time_created: datetime = Field(default_factory=datetime.now)