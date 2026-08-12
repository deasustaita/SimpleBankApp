from models.Account import Account
from typing import Optional, List
from repositories.CustomerRepository import CustomerRepository
from bson import ObjectId

class AccountRepository:
    def __init__(self, customer_repo: CustomerRepository, database):
        self.customer_repo = customer_repo
        self._accounts = database["Account"]

    def create_account(self, customer_id: str, account: Account) -> Optional[Account]:
        customer = self.customer_repo.find_by_id(customer_id)

        if not customer:
            return None

        account.customer_id = customer_id

        account_data = account.model_dump(by_alias=True, exclude_none=True)
        result = self._accounts.insert_one(account_data)
        
        account.account_id = str(result.inserted_id)
        return account

    def find_by_id(self, account_id: str) -> Optional[Account]:
        if not ObjectId.is_valid(account_id):
            return None

        account = self._accounts.find_one({"_id": ObjectId(account_id)})

        if account:
            return Account(**account)
        return None

    def find_accounts(self) -> List[Account]:
        accounts = self._accounts.find()
        return [Account(**acc) for acc in accounts]

    def find_accounts_by_customer(self, customer_id: str) -> List[Account]:
        customer = self.customer_repo.find_by_id(customer_id)

        if not customer:
            return None

        accounts = self._accounts.find({"customer_id": customer_id})
        return [Account(**acc) for acc in accounts]


    def remove_account(self, account_id: str):
        if not ObjectId.is_valid(account_id):
            return None

        result = self._accounts.delete_one(
            {"_id": ObjectId(account_id)}
        )

        return result.deleted_count > 0