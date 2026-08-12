from pydantic import BaseModel, Field, Discriminator
from datetime import datetime
from decimal import Decimal
from typing import Literal, Annotated, Union

class TransactionBase(BaseModel):
    txn_id: int
    account_id: int

    amount: Decimal
    created_at: datetime = Field(default_factory=datetime.now)

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