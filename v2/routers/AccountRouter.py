from fastapi import APIRouter, HTTPException, status

from repositories.AccountRepository import AccountRepository
from services.AccountService import AccountService
from models.Account import Account
from schemas.ResponseEntity import ResponseEntity

router = APIRouter()

repo = AccountRepository()
service = AccountService(repo)

@router.post("/", response_model=ResponseEntity[Account])
def open_new_account(customer_id: int, account: Account):
    new_account = service.create_account(customer_id, account)
    return ResponseEntity(
        status_code=status.HTTP_201_CREATED,
        message="Created new account successfully.",
        data=new_account
    )

@router.get("/{account_id}", response_model=ResponseEntity[Account])
def get_account_by_id(account_id: int):
    account = service.get_account_by_id(account_id)
    if not account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Account not found."
        )
    return ResponseEntity(
        status_code=status.HTTP_200_OK,
        message="Account found.",
        data=account
    )