from typing import List, Optional
from repositories import CustomerRepository
from models.Customer import Customer

class CustomerService:
    def __init__(self, repository: CustomerRepository):
        self.repository = repository

    def get_all_customers(self) -> List[Customer]:
        return self.repository.find_customers()

    def get_customer_by_id(self, customer_id: int) -> Optional[Customer]:
        return self.repository.find_by_id(customer_id)

    def create_customer(self, customer: Customer) -> Customer:
        return self.repository.make_customer(customer)

    def update_customer(self, customer_id: int, customer: Customer) -> Optional[Customer]:
        return self.repository.update_customer(customer_id, customer)

    def delete_customer(self, customer_id: int) -> bool:
        return self.repository.remove_customer(customer_id)