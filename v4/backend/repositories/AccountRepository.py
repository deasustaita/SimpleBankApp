from models.Account import Account
from typing import Optional, List
from repositories.CustomerRepository import CustomerRepository
from bson import ObjectId
from pydantic import TypeAdapter
from decimal import Decimal
from bson.decimal128 import Decimal128

account_adapter = TypeAdapter(Account)

class AccountRepository:
    def __init__(self, customer_repo: CustomerRepository, database):
        self.customer_repo = customer_repo
        self._accounts = database["Account"]

    def _prepare_document(self, doc: dict) -> dict:
        if not doc:
            return doc
        if "acc_type" in doc and isinstance(doc["acc_type"], str):
            doc["acc_type"] = doc["acc_type"].upper()
        for key, value in doc.items():
            if isinstance(value, Decimal128):
                doc[key] = value.to_decimal()
        return doc

    def create_account(self, customer_id: str, account: Account) -> Optional[Account]:
        customer = self.customer_repo.find_by_id(customer_id)

        if not customer:
            return None

        account.customer_id = customer_id
        account_data = account.model_dump(by_alias=True, exclude_none=True)

        if "balance" in account_data and isinstance(account_data["balance"], Decimal):
            account_data["balance"] = Decimal128(account_data["balance"])

        result = self._accounts.insert_one(account_data)
        
        account.account_id = str(result.inserted_id)
        return account

    def find_by_id(self, account_id: str) -> Optional[Account]:
        if not ObjectId.is_valid(account_id):
            return None

        account = self._accounts.find_one({"_id": ObjectId(account_id)})

        if account:
            return account_adapter.validate_python(self._prepare_document(account))
        return None

    def find_accounts(self) -> List[Account]:
        accounts = self._accounts.find()
        return account_adapter.validate_python(self._prepare_document(acc) for acc in accounts)


    def find_accounts_by_customer(self, customer_id: str) -> Optional[List[Account]]:
        customer = self.customer_repo.find_by_id(customer_id)

        if not customer:
            return []

        accounts = self._accounts.find({"customer_id": customer_id})

        return [account_adapter.validate_python(self._prepare_document(acc)) for acc in accounts]

    def remove_account(self, account_id: str):
        if not ObjectId.is_valid(account_id):
            return None

        result = self._accounts.delete_one(
            {"_id": ObjectId(account_id)}
        )

        return result.deleted_count > 0