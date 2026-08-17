from fastapi import APIRouter, HTTPException, status, Request, Depends

from typing import List
from auth.jwt import get_current_customer_id

from repositories.AccountRepository import AccountRepository
from repositories.CustomerRepository import CustomerRepository

from services.AccountService import AccountService
from models.Account import Account, AccountUpdate
from models.ResponseEntity import ResponseEntity

router = APIRouter()


def _ensure_customer_access(requested_customer_id: str, current_customer_id: str):
    if requested_customer_id != current_customer_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not allowed to access this customer's accounts."
        )


def _get_owned_account_or_404(service: AccountService, account_id: str, current_customer_id: str) -> Account:
    account = service.get_account_by_id(account_id)

    if not account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"An account with ID #{account_id} does not exist."
        )

    if account.customer_id != current_customer_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not allowed to access this account."
        )

    return account

@router.post("/{customer_id}/accounts", response_model=ResponseEntity[Account])
def open_new_account(customer_id: str, account: Account, request: Request, current_customer_id: str = Depends(get_current_customer_id)):
    _ensure_customer_access(customer_id, current_customer_id)

    cust_repo = CustomerRepository(request.app.database)
    repository = AccountRepository(cust_repo, request.app.database)
    service = AccountService(repository)

    new_account = service.create_account(customer_id, account)

    return ResponseEntity(
        status_code=status.HTTP_201_CREATED,
        message="Created new account successfully.",
        data=new_account
    )

@router.get("/accounts/{account_id}", response_model=ResponseEntity[Account])
def get_account_by_id(account_id: str, request: Request, current_customer_id: str = Depends(get_current_customer_id)):
    cust_repo = CustomerRepository(request.app.database)
    repository = AccountRepository(cust_repo, request.app.database)
    service = AccountService(repository)

    account = _get_owned_account_or_404(service, account_id, current_customer_id)

    return ResponseEntity(
        status_code=status.HTTP_200_OK,
        message="Account found.",
        data=account
    )

@router.get("/accounts", response_model=ResponseEntity[List[Account]])
def get_all_accounts(request: Request, current_customer_id: str = Depends(get_current_customer_id)):
    cust_repo = CustomerRepository(request.app.database)
    repository = AccountRepository(cust_repo, request.app.database)
    service = AccountService(repository)

    accounts = service.get_customer_accounts(current_customer_id)

    return ResponseEntity(
        status_code=status.HTTP_200_OK,
        message="Accounts retrieved successfully.",
        data=accounts
    )

@router.get("/{customer_id}/accounts", response_model=ResponseEntity[List[Account]])
def get_customer_accounts(customer_id: str, request: Request, current_customer_id: str = Depends(get_current_customer_id)):
    _ensure_customer_access(customer_id, current_customer_id)

    cust_repo = CustomerRepository(request.app.database)
    repository = AccountRepository(cust_repo, request.app.database)
    service = AccountService(repository)

    accounts = service.get_customer_accounts(customer_id)

    return ResponseEntity(
        status_code=status.HTTP_200_OK,
        message="Accounts retrieved successfully.",
        data=accounts
    )

@router.delete("/accounts/{account_id}", response_model=ResponseEntity)
def delete_account(account_id: str, request: Request, current_customer_id: str = Depends(get_current_customer_id)):
    cust_repo = CustomerRepository(request.app.database)
    repository = AccountRepository(cust_repo, request.app.database)
    service = AccountService(repository)

    _get_owned_account_or_404(service, account_id, current_customer_id)

    deleted = service.delete_account(account_id)

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Account not found."
        )
    return ResponseEntity(
        status_code=status.HTTP_200_OK,
        message="Account deleted."
    )

@router.patch("/accounts/{account_id}", response_model=ResponseEntity[Account])
def update_account_settings(account_id: str, update: AccountUpdate, request: Request, current_customer_id: str = Depends(get_current_customer_id)):
    cust_repo = CustomerRepository(request.app.database)
    repository = AccountRepository(cust_repo, request.app.database)
    service = AccountService(repository)

    _get_owned_account_or_404(service, account_id, current_customer_id)

    updated = service.update_account(account_id, update.model_dump(exclude_unset=True))

    if not updated:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"An account with ID #{account_id} does not exist."
        )
    return ResponseEntity(
        status_code=status.HTTP_200_OK,
        message="Account updated successfully.",
        data=updated
    )