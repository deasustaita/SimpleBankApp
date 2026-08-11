from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse

from repositories.CustomerRepository import CustomerRepository
from services.CustomerService import CustomerService
from models.Customer import Customer

router = APIRouter()

repo = CustomerRepository()
service = CustomerService(repo)

@router.get("/")
def get_all_customers():
    customers = service.get_all_customers()
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=[Customer(**c).model_dump() for c in customers],
    )


@router.get("/{customer_id}")
def get_customer_by_id(customer_id: int):
    customer = service.get_customer_by_id(customer_id)
    if not customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found"
        )
    return JSONResponse(
        status_code=status.HTTP_200_OK, content=customer.model_dump()
    )

@router.post("/", status_code=status.HTTP_201_CREATED)
def create_customer_profile(customer: Customer):
    return service.create_customer(customer)