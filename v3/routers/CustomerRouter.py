from fastapi import APIRouter, Request, HTTPException, status
from repositories.CustomerRepository import CustomerRepository
from services.CustomerService import CustomerService
from models.Customer import Customer

router = APIRouter()


@router.get("/")
def get_all_customers(request: Request):
    repository = CustomerRepository(request.app.database)
    service = CustomerService(repository)

    return service.get_all_customers()


@router.get("/{customer_id}")
def get_customer_by_id(customer_id: int, request: Request):
    repository = CustomerRepository(request.app.database)
    service = CustomerService(repository)

    customer = service.get_customer_by_id(customer_id)

    if customer is not None:
        return customer
    
    raise HTTPException( 
        status_code=status.HTTP_404_NOT_FOUND, 
        detail=f"A customer with ID #{customer_id} does not exist."
    )

@router.post("/", status_code=status.HTTP_201_CREATED)
def create_customer_profile(customer: Customer, request: Request):
    repository = CustomerRepository(request.app.database)
    service = CustomerService(repository)

    return service.create_customer(customer)

@router.put("/")
def edit_customer_profile(customer: Customer, request: Request):
    pass

@router.delete("/")
def delete_customer(customer: Customer, request: Request):
    pass