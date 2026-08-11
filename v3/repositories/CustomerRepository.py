from models.Customer import Customer
from typing import List, Optional


# manipulation of data occurs here
class CustomerRepository:
    def __init__(self,database):
        self.collection = database["Customer"]

    def find_customers(self) -> List[Customer]:
        # return the data of all customers in the database
        customers = self.collection.find({}, {"_id": 0})
        return [Customer(**customer) for customer in customers]

    def find_by_id(self, customer_id: int) -> Optional[Customer]:
        customer = self.collection.find_one({"id":customer_id}, {"_id": 0})
        if customer is None:
            return None
        return Customer(**customer)

    def make_customer(self, customer: Customer) -> Customer:
        self.collection.insert_one(customer.model_dump())
        return customer

## wrap in a ResponseEntity rather than return a list
# 1 example of getall getbyid post put delete rest method call(controller -> service -> repo) 