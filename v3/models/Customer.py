from pydantic import BaseModel, EmailStr, Field
from datetime import datetime

# use mongoengine for orm data

class Customer(BaseModel):
    id: int
    username: str
    password: str

    name: str
    email: EmailStr # must be unique
    # accounts: list[Account] = Field(default_factory=list)

    time_created: datetime = Field(default_factory=datetime.now)
