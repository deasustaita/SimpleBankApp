from pydantic import BaseModel, Field, ConfigDict
from decimal import Decimal
from datetime import datetime, timezone
from typing import Optional, Annotated
from pydantic.functional_validators import BeforeValidator

PyObjectID = Annotated[str, BeforeValidator(str)]

class Account(BaseModel):
    account_id: Optional[PyObjectID] = Field(alias="_id", default=None)
    customer_id: Optional[str] = None
    
    balance: Decimal = Field(default=0.0)
    account_type: str

    time_created: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True
    )