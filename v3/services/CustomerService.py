from typing import List, Optional
from repositories import CustomerRepository
from models import Customer

class CustomerService:
    def __init__(self, repository: CustomerRepository):
        self.repository = repository

    def get_all_customers(self) -> List[Customer]:
        return self.repository.find_customers()

    def get_customer_by_id(self, customer_id: int) -> Optional[Customer]:
        return self.repository.find_by_id(customer_id)

    