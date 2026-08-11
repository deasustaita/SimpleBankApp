# from fastapi import FastAPI, status, HTTPException
# from services.CustomerService import CustomerService
# from typing import List
# from models.Customer import Customer
# from repositories.CustomerRepository import CustomerRepository
# from fastapi.responses import JSONResponse

# app = FastAPI()

# repository = CustomerRepository()
# service = CustomerService()

# @app.get("/api/v1/customers")
# def get_all_customers():
#     customers: List[Customer] = service.get_all_customers()

#     return JSONResponse(
#         status_code=status.HTTP_200_OK,
#         content=[c.model_dump() for c in customers],
#         headers={"X-Total-Count": str(len(customers))}
#     )

# @app.get("/api/v1/customers/{id}")
# def get_customer_by_id(customer_id: int):
#     customer = service.get_costumer_by_id(customer_id)

#     if not customer:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found."
#         )

#     return JSONResponse(
#         status_code=status.HTTP_200_OK, content=customer.model_dump()
#     )