from typing import List, Optional
from repositories.CustomerRepository import CustomerRepository
from models.Customer import Customer


class CustomerService:
    def __init__(self, repository: CustomerRepository):
        self.repository = repository

    def get_all_customers(self) -> List[Customer]:
        return self.repository.find_customers()

    def get_customer_by_id(self, customer_id: str) -> Optional[Customer]:
        return self.repository.find_by_id(customer_id)

    def create_customer(self, customer: Customer) -> Customer:
        return self.repository.make_customer(customer)

    def update_customer(self, customer_id: str, customer: Customer) -> Optional[Customer]:
        return self.repository.update_customer(customer_id, customer)

    def delete_customer(self, customer_id: str) -> bool:
        return self.repository.remove_customer(customer_id)

    def authenticate_customer(self, username: str, password: str) -> Optional[Customer]:
        customer = self.repository.find_by_username(username)

        if not customer or customer.password != password:
            return None

        return customer