from models.Account import Account
from typing import List, Optional
from repositories.CustomerRepository import CustomerRepository

class AccountRepository:
    def __init__(self, customer_repo: CustomerRepository):
        self.customer_repo = customer_repo

    def create_account(self, customer_id: int, account: Account) -> Optional[Account]:
        customer = self.customer_repo.find_by_id(customer_id)

        if not customer:
            return None

        account.user_id = customer_id
        
        customer.accounts.append(account)
        return account