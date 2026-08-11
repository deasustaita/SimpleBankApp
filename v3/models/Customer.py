from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
import uuid

# use mongoengine for orm data

class Customer(BaseModel):
    id: int
    username: str

    ## For use in later developments but for the moment only the above is needed.
    # name: str
    # password: str
    # created_at: datetime # default current timestamp
    # email: EmailStr # has to be unique
    # uuid for id

