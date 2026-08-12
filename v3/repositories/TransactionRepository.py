from models.Transaction import Transaction
from typing import Optional
from repositories.AccountRepository import AccountRepository

class TransactionRepository():
    def __init__(self, account_repo: AccountRepository, database):
        self.account_repo = account_repo
        self._transactions = database["Transaction"]

    def find_transactions(self): # CHANGE THIS SO ITS TAKING FROM ALL THE CUSTOMER'S ACCOUNTS
        transactions = self._transactions.find()
        return [Transaction(**txn) for txn in transactions]

    def transfer_money(self, account_id: int, transfer: Transaction) -> Optional[Transaction]:
        account = self.account_repo.find_by_id(account_id)

        if not account:
            return None

        transfer.account_id = account_id

        transfer_data = transfer.model_dump(by_alias=True, exclude_none=True)
        result = self._transactions.insert_one(transfer_data)

        transfer.account_id = str(result.inserted_id)
        return transfer

    def deposit_money(self, account_id: int, deposit: Transaction) -> Optional[Transaction]:
        account = self.account_repo.find_by_id(account_id)

        if not account:
            return None

        deposit.account_id = account_id
        
        deposit_data = deposit.model_dump(by_alias=True, exclude_none=True)
        result = self._transactions.insert_one(deposit_data)

        deposit.account_id = str(result.inserted_id)
        return deposit

    def withdraw_money(self, account_id: int, withdrawal: Transaction) -> Optional[Transaction]:
        account = self.account_repo.find_by_id(account_id)

        if not account:
            return None

        withdrawal.account_id = account_id

        withdrawal_data = withdrawal.model_dump(by_alias=True, exclude_none=True)
        result = self._transactions.insert_one(withdrawal_data)

        withdrawal.account_id = str(result.inserted_id)
        return withdrawal