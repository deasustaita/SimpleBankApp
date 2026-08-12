from fastapi import APIRouter, HTTPException, status, Request

from typing import List, Optional

from repositories.AccountRepository import AccountRepository
from repositories.CustomerRepository import CustomerRepository
from services.AccountService import AccountService
from models.Account import Account
from schemas.ResponseEntity import ResponseEntity

router = APIRouter()

@router.post("/{customer_id}/accounts", response_model=ResponseEntity[Account])
def open_new_account(customer_id: str, account: Account, request: Request):
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
def get_account_by_id(account_id: str, request: Request):
    cust_repo = CustomerRepository(request.app.database)
    repository = AccountRepository(cust_repo, request.app.database)
    service = AccountService(repository)
    
    account = service.get_account_by_id(account_id)

    if not account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"A customer with ID #{account_id} does not exist."
        )
    return ResponseEntity(
        status_code=status.HTTP_200_OK,
        message="Account found.",
        data=account
    )

@router.get("/accounts", response_model=ResponseEntity[List[Account]])
def get_all_accounts(request: Request):
    cust_repo = CustomerRepository(request.app.database)
    repository = AccountRepository(cust_repo, request.app.database)
    service = AccountService(repository)

    accounts = service.get_all_accounts()

    return ResponseEntity(
        status_code=status.HTTP_200_OK,
        message="Accounts retrieved successfully.",
        data=accounts
    )

@router.get("/{customer_id}/accounts", response_model=ResponseEntity[List[Account]])
def get_customer_accounts(customer_id: str, request: Request):
    cust_repo = CustomerRepository(request.app.database)
    repository = AccountRepository(cust_repo, request.app.database)
    service = AccountService(repository)

    accounts = service.get_customer_accounts(customer_id)

    if not accounts:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"A customer with ID #{customer_id} does not exist."
        )
    return ResponseEntity(
        status_code=status.HTTP_200_OK,
        message="Accounts retrieved successfully.",
        data=accounts
    )

@router.delete("accounts/{account_id}", response_model=ResponseEntity)
def delete_account(account_id: str, request: Request):
    cust_repo = CustomerRepository(request.app.database)
    repository = AccountRepository(cust_repo, request.app.database)
    service = AccountService(repository)

    deleted = service.delete_account(account_id)

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found."
        )
    return ResponseEntity(
        status_code=status.HTTP_200_OK,
        message="Customer deleted."
    )