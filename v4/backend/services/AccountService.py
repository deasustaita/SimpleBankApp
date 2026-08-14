from typing import Optional, List
from models.Account import Account
from repositories.AccountRepository import AccountRepository

class AccountService:
    def __init__(self, repository: AccountRepository):
        self.repository = repository

    def create_account(self, customer_id: str, account: Account) -> Account:
        return self.repository.create_account(customer_id, account)

    def get_account_by_id(self, account_id: str) -> Optional[Account]:
        return self.repository.find_by_id(account_id)

    def get_all_accounts(self) -> List[Account]:
        return self.repository.find_accounts()

    def get_customer_accounts(self, customer_id: str) -> Optional[List[Account]]:
        return self.repository.find_accounts_by_customer(customer_id)

    def delete_account(self, account_id: str) -> bool:
        return self.repository.remove_account(account_id)

    def update_account(self, account_id: str, updates: dict) -> Optional[Account]:
        return self.repository.update_account(account_id, updates)