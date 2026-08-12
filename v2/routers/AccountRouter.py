from fastapi import APIRouter

from repositories.AccountRepository import AccountRepository
from services.AccountService import AccountService
from models.Account import Account
from schemas.ResponseEntity import ResponseEntity

router = APIRouter()

repo = AccountRepository()
service = AccountService(repo)

@router.post("/", response_model=ResponseEntity[Account])
def open_new_account():
    pass
 