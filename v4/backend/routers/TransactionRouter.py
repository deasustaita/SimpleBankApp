from fastapi import APIRouter, HTTPException, status, Request, Depends

from typing import List
from auth.jwt import get_current_customer_id

from repositories.TransactionRepository import TransactionRepository
from repositories.AccountRepository import AccountRepository
from repositories.CustomerRepository import CustomerRepository

from services.TransactionService import TransactionService
from models.Transaction import Transaction
from models.ResponseEntity import ResponseEntity

router = APIRouter()


def _ensure_customer_access(requested_customer_id: str, current_customer_id: str):
    if requested_customer_id != current_customer_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not allowed to access this customer's transactions."
        )


def _ensure_account_access(request: Request, account_id: str, current_customer_id: str):
    cust_repo = CustomerRepository(request.app.database)
    acc_repo = AccountRepository(cust_repo, request.app.database)
    account = acc_repo.find_by_id(account_id)

    if not account:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Account not found.")

    if account.customer_id != current_customer_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not allowed to access this account."
        )

def _build_service(request: Request) -> TransactionService:
    cust_repo = CustomerRepository(request.app.database)
    acc_repo = AccountRepository(cust_repo, request.app.database)
    repository = TransactionRepository(acc_repo, request.app.database)
    return TransactionService(repository)

@router.get("/", response_model=ResponseEntity[List[Transaction]])
def get_transactions(request: Request, current_customer_id: str = Depends(get_current_customer_id)):
    service = _build_service(request)

    transactions = service.get_transactions_by_customer(current_customer_id)

    return ResponseEntity(
        status_code=status.HTTP_200_OK,
        message="Transactions retrieved successfully.",
        data=transactions
    )

@router.get("/account/{account_id}", response_model=ResponseEntity[List[Transaction]])
def get_account_transactions(account_id: str, request: Request, current_customer_id: str = Depends(get_current_customer_id)):
    _ensure_account_access(request, account_id, current_customer_id)

    service = _build_service(request)

    transactions = service.get_transactions_by_account(account_id)

    return ResponseEntity(
        status_code=status.HTTP_200_OK,
        message="Account transactions retrieved successfully.",
        data=transactions
    )

@router.get("/customer/{customer_id}", response_model=ResponseEntity[List[Transaction]])
def get_customer_transactions(customer_id: str, request: Request, current_customer_id: str = Depends(get_current_customer_id)):
    _ensure_customer_access(customer_id, current_customer_id)

    service = _build_service(request)

    transactions = service.get_transactions_by_customer(customer_id)

    return ResponseEntity(
        status_code=status.HTTP_200_OK,
        message="Customer transactions retrieved successfully.",
        data=transactions
    )

@router.post("/transfer", response_model=ResponseEntity[Transaction])
def process_money_transfer(account_id: str, transaction: Transaction, request: Request, current_customer_id: str = Depends(get_current_customer_id)):
    _ensure_account_access(request, account_id, current_customer_id)

    service = _build_service(request)

    try:
        new_transfer = service.transfer_money(account_id, transaction)
    except ValueError as error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(error))

    if not new_transfer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Account not found.")

    return ResponseEntity(
        status_code=status.HTTP_201_CREATED,
        message="Money transferred successfully.",
        data=new_transfer
    )

@router.post("/deposit", response_model=ResponseEntity[Transaction])
def process_deposit(account_id: str, transaction: Transaction, request: Request, current_customer_id: str = Depends(get_current_customer_id)):
    _ensure_account_access(request, account_id, current_customer_id)

    service = _build_service(request)

    new_deposit = service.deposit_money(account_id, transaction)

    if not new_deposit:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Account not found.")

    return ResponseEntity(
        status_code=status.HTTP_201_CREATED,
        message="Money deposited successfully.",
        data=new_deposit
    )

@router.post("/withdrawal", response_model=ResponseEntity[Transaction])
def process_withdrawal(account_id: str, transaction: Transaction, request: Request, current_customer_id: str = Depends(get_current_customer_id)):
    _ensure_account_access(request, account_id, current_customer_id)

    service = _build_service(request)

    try:
        new_withdrawal = service.withdraw_money(account_id, transaction)
    except ValueError as error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(error))

    if not new_withdrawal:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Account not found.")

    return ResponseEntity(
        status_code=status.HTTP_201_CREATED,
        message="Money withdrew successfully.",
        data=new_withdrawal
    )