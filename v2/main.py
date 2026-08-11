from fastapi import FastAPI, HTTPException, status
from fastapi.responses import JSONResponse

from repositories.CustomerRepository import CustomerRepository
from services.CustomerService import CustomerService

app = FastAPI()

# Instantiate the service and repository directly
repository = CustomerRepository()
service = CustomerService(repository=repository)


@app.get("/api/v1/customers")
def get_all_customers():
    customers = service.get_all_customers()
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=[c.model_dump() for c in customers],
    )


@app.get("/api/v1/customers/{customer_id}")
def get_customer_by_id(customer_id: int):
    customer = service.get_customer_by_id(customer_id)
    if not customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found"
        )
    return JSONResponse(
        status_code=status.HTTP_200_OK, content=customer.model_dump()
    )

# post create customer profile

# get list customers

# get customer details
# MAIN.PY SHOULD BE IN CONTROLLERS NOT MODELS?


# MODELS WILL NOT INCLUDE THE DATABASE RN
# IT WILL BE HARD-CODED