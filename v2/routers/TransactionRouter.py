from fastapi import APIRouter, status

from repositories.TransactionRepository import TransactionRepository
from services.TransactionService import TransactionService
from models.Transaction import Transaction
from schemas.ResponseEntity import ResponseEntity

router = APIRouter()

repo = TransactionRepository()
service = TransactionService(repo)

@router.post("/transfer", response_model=ResponseEntity[Transaction])
def process_money_transfer(account_id: int, transaction: Transaction):
    new_transfer = service.transfer_money(account_id, transaction)
    return ResponseEntity(
        status_code=status.HTTP_201_CREATED,
        message="Money transferred successfully.",
        data=new_transfer
    )

@router.post("/deposit", response_model=ResponseEntity([Transaction]))
def process_deposit(account_id: int, transaction: Transaction):
    new_deposit = service.deposit_money(account_id, transaction)
    return ResponseEntity(
        status_code=status.HTTP_201_CREATED,
        message="Money transferred successfully.",
        data=new_deposit
    )

@router.post("/withdrawal", response_model=ResponseEntity([Transaction]))
def process_withdrawal(account_id:int, transaction: Transaction):
    new_withdrawal = service.withdraw_money(account_id, transaction)
    return ResponseEntity(
        status_code=status.HTTP_201_CREATED,
        message="Money withdrew successfully.",
        data=new_withdrawal
    )