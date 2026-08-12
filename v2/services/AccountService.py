from typing import Optional
from models.Account import Account
from repositories.AccountRepository import AccountRepository

class AccountService:
    def __init__(self, repository: AccountRepository):
        self.repository = repository

    def create_account(self, customer_id: int, account: Account) -> Account:
        return self.repository.create_account(customer_id, account)

    def get_account_by_id(self, account_id: int) -> Optional[Account]:
        return self.repository.find_by_id(account_id)