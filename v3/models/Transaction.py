from pydantic import BaseModel, Field, Discriminator, ConfigDict
from datetime import datetime
from decimal import Decimal
from typing import Literal, Annotated, Union, Optional
from pydantic.functional_validators import BeforeValidator


PyObjectID = Annotated[str, BeforeValidator(str)]

class TransactionBase(BaseModel):
    txn_id: Optional[PyObjectID] = Field(alias="_id", default=None)
    account_id: Optional[str] = None

    amount: Decimal
    created_at: datetime = Field(default_factory=datetime.now)

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True
    )

class Deposit(TransactionBase):
    txn_type: Literal["DEPOSIT"]

class Withdrawal(TransactionBase):
    txn_type: Literal["WITHDRAWAL"]

class Transfer(TransactionBase):
    txn_type: Literal["TRANSACTION"]
    dest_account_id: int

Transaction = Annotated[
    Union[Deposit, Transfer, Withdrawal],
    Discriminator("txn_type")
]