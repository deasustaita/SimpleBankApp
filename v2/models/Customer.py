from pydantic import BaseModel, EmailStr, Field
from models.Account import Account
from datetime import datetime

class Customer(BaseModel):
    id: int # change to random generation
    username: str
    password: str

    name: str
    email: EmailStr
    accounts: list[Account] = Field(default_factory=list)

    time_created: datetime = Field(default_factory=datetime.now)
