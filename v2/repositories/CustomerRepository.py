from models import Customer
from sample_data import customers
from typing import List, Optional


# manipulation of data occurs here
class CustomerRepository:
    def __init__(self):
        self._data: List[Customer] = customers

    def find_customers(self) -> List[Customer]:
        # return the data of all customers in the database
        return self._data

    def find_by_id(self, customer_id: int) -> Optional[Customer]:
        for customer in customers:
            if customer.id == customer_id:
                return customer
        return None

## wrap in a ResponseEntity rather than return a list
# 1 example of getall getbyid post put delete rest method call(controller -> service -> repo)