from fastapi import APIRouter, Request, HTTPException, status, Depends
from typing import List

from auth.jwt import create_access_token, get_current_customer_id

from repositories.CustomerRepository import CustomerRepository
from services.CustomerService import CustomerService
from models.Customer import Customer, CustomerUpdateRequest
from models.ResponseEntity import ResponseEntity
from models.Login import LoginCredentialsRequest

router = APIRouter()


def _ensure_customer_access(requested_customer_id: str, current_customer_id: str):
    if requested_customer_id != current_customer_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not allowed to access this customer profile."
        )


@router.post("/login")
def login_customer(credentials: LoginCredentialsRequest, request: Request):
    repository = CustomerRepository(request.app.database)
    service = CustomerService(repository)

    customer = service.authenticate_customer(credentials.username, credentials.password)

    if not customer:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid username or password.'
        )

    token = create_access_token(customer.id)
    
    return ResponseEntity(
        status_code=status.HTTP_200_OK,
        message="Login successful.",
        data={"access_token": token, "token_type": "bearer"}
    )


@router.get("/", response_model=ResponseEntity[List[Customer]])
def get_all_customers(request: Request, _: str = Depends(get_current_customer_id)):
    repository = CustomerRepository(request.app.database)
    service = CustomerService(repository)

    customers = service.get_all_customers()

    return ResponseEntity(
        status_code=status.HTTP_200_OK,
        message="Customers retrieved successfully.",
        data=customers
    )

@router.get("/me", response_model=ResponseEntity[Customer])
def get_current_customer_profile(request: Request, customer_id: str = Depends(get_current_customer_id)):
    repository = CustomerRepository(request.app.database)
    service = CustomerService(repository)

    customer = service.get_customer_by_id(customer_id)

    if not customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found."
        )
    return ResponseEntity(
        status_code=status.HTTP_200_OK,
        message="Customer found.",
        data=customer
    )


@router.get("/{customer_id}", response_model=ResponseEntity[Customer])
def get_customer_by_id(customer_id: str, request: Request, current_customer_id: str = Depends(get_current_customer_id)):
    _ensure_customer_access(customer_id, current_customer_id)

    repository = CustomerRepository(request.app.database)
    service = CustomerService(repository)

    customer = service.get_customer_by_id(customer_id)

    if not customer:
        raise HTTPException( 
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"A customer with ID #{customer_id} does not exist."
        )
    return ResponseEntity(
        status_code=status.HTTP_200_OK,
        message="Customer found.",
        data=customer
    )


@router.post("/", response_model=ResponseEntity[Customer])
def create_customer_profile(customer: Customer, request: Request):
    repository = CustomerRepository(request.app.database)
    service = CustomerService(repository)

    try:
        created_customer = service.create_customer(customer)
    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(error)
        )

    return ResponseEntity(
        status_code=status.HTTP_201_CREATED,
        message="Customer created successfully.",
        data=created_customer
    )


@router.put("/{customer_id}", response_model=ResponseEntity[Customer])
def update_customer_info(customer_id: str, customer: Customer, request: Request, current_customer_id: str = Depends(get_current_customer_id)):
    _ensure_customer_access(customer_id, current_customer_id)

    repository = CustomerRepository(request.app.database)
    service = CustomerService(repository)

    try:
        updated_customer = service.update_customer(customer_id, customer.model_dump(exclude_none=True, by_alias=True))
    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(error)
        )

    if not updated_customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found."
        )
    return ResponseEntity(
        status_code=status.HTTP_200_OK,
        message="Customer information updated.",
        data=updated_customer
    )


@router.patch("/me", response_model=ResponseEntity[Customer])
def update_current_customer_info(
    updates: CustomerUpdateRequest,
    request: Request,
    customer_id: str = Depends(get_current_customer_id)
):
    repository = CustomerRepository(request.app.database)
    service = CustomerService(repository)

    try:
        updated_customer = service.update_customer(customer_id, updates.model_dump(exclude_none=True))
    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(error)
        )

    if not updated_customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found."
        )

    return ResponseEntity(
        status_code=status.HTTP_200_OK,
        message="Customer profile updated.",
        data=updated_customer
    )

@router.delete("/me", response_model=ResponseEntity)
def delete_current_customer(request: Request, customer_id: str = Depends(get_current_customer_id)):
    repository = CustomerRepository(request.app.database)
    service = CustomerService(repository)

    deleted = service.delete_customer(customer_id)

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found."
        )

    return ResponseEntity(
        status_code=status.HTTP_200_OK,
        message="Customer deleted."
    )


@router.delete("/{customer_id}", response_model=ResponseEntity)
def delete_customer(customer_id: str, request: Request, current_customer_id: str = Depends(get_current_customer_id)):
    _ensure_customer_access(customer_id, current_customer_id)

    repository = CustomerRepository(request.app.database)
    service = CustomerService(repository)

    deleted = service.delete_customer(customer_id)

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found."
        )
    return ResponseEntity(
        status_code=status.HTTP_200_OK,
        message="Customer deleted."
    )