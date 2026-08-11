from pydantic import BaseModel, EmailStr
from models.Account import Account
from datetime import datetime

class Customer(BaseModel):
    id: int # change to random generation
    username: str
    password: str

    name: str
    email: EmailStr
    accounts: list[Account]

    time_created: str
