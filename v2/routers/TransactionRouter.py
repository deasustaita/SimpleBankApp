from fastapi import APIRouter

from repositories.TransactionRepository import TransactionRepository
from services.TransactionService import TransactionService
from models.Transaction import Transaction
from schemas.ResponseEntity import ResponseEntity

router = APIRouter()

repo = TransactionRepository()
service = TransactionService(repo)

@router.post("/transfer", response_model=ResponseEntity[Transaction])
def process_money_transfer():
    pass