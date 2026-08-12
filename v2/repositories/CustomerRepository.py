from models.Customer import Customer
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
        for _idx, customer in enumerate(self._data):
            if customer.id == customer_id:
                return customer
        return None

    def make_customer(self, customer: Customer) -> Customer:
        self._data.append(customer)
        return customer

    def update_customer(self, customer_id: int, up_customer: Customer) -> Optional[Customer]:
        for index, customer in enumerate(self._data):
            if customer.id == customer_id:
                up_customer.id = customer_id
                self._data[index] = up_customer
                return up_customer
        return None

    def remove_customer(self, customer_id: int):
        for index, customer in enumerate(self._data):
            if customer.id == customer_id:
                self._data.pop(index)
                return True
        return False

## wrap in a ResponseEntity rather than return a list
# 1 example of getall getbyid post put delete rest method call(controller -> service -> repo)