from fastapi import APIRouter, Request, HTTPException, status

from repositories.CustomerRepository import CustomerRepository
from services.CustomerService import CustomerService
from models.Customer import Customer
from schemas.ResponseEntity import ResponseEntity

router = APIRouter()


@router.get("/", response_model=ResponseEntity[Customer])
def get_all_customers(request: Request):
    repository = CustomerRepository(request.app.database)
    service = CustomerService(repository)

    customers = service.get_all_customers()

    return ResponseEntity(
        status_code=status.HTTP_200_OK,
        message="Customers retrieved successfully.",
        data=customers
    )


@router.get("/{customer_id}", response_model=ResponseEntity[Customer])
def get_customer_by_id(customer_id: int, request: Request):
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

    created_customer = service.create_customer(customer)

    return ResponseEntity(
        status_code=status.HTTP_201_CREATED,
        message="Customer created successfully.",
        data=created_customer
    )


@router.put("/{customer_id}", response_model=ResponseEntity[Customer])
def update_customer_info(customer_id: int, customer: Customer, request: Request):
    repository = CustomerRepository(request.app.database)
    service = CustomerService(repository)

    updated_customer = service.update_customer(customer_id, customer)

    if not updated_customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found."
        )
    return ResponseEntity(
        status_code=status.HTTP_200_OK,
        message="Customer information updated.",
        data=updated_customer
    )

@router.delete("/{customer_id}", response_model=ResponseEntity[Customer])
def delete_customer(customer_id: int, request: Request):
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