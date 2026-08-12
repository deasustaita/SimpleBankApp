from models.Account import Account
from typing import Optional, Dict
from repositories.CustomerRepository import CustomerRepository

class AccountRepository:
    def __init__(self, customer_repo: CustomerRepository):
        self.customer_repo = customer_repo
        self._accounts: Dict[int, Account] = {}

    def create_account(self, customer_id: int, account: Account) -> Optional[Account]:
        customer = self.customer_repo.find_by_id(customer_id)

        if not customer:
            return None

        account.user_id = customer_id
        
        customer.accounts.append(account)
        self._accounts[account.id] = account

        return account

    def find_by_id(self, account_id: int) -> Optional[Account]:
        return self._accounts.get(account_id)