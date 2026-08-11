from fastapi import APIRouter, Request, HTTPException, status
from repositories.CustomerRepository import CustomerRepository
from services.CustomerService import CustomerService

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