from pydantic import BaseModel, EmailStr, Field, ConfigDict
from pydantic.functional_validators import BeforeValidator
from typing import Annotated, Optional
from datetime import datetime, timezone

# use mongoengine for orm data

PyObjectID = Annotated[str, BeforeValidator(str)]

class Customer(BaseModel):
    id: Optional[PyObjectID] = Field(alias="_id", default=None)
    username: str
    password: str

    name: str
    email: EmailStr # must be unique

    time_created: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True
    )