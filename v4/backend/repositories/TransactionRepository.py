from models.Transaction import Transaction
from typing import List, Optional
from repositories.AccountRepository import AccountRepository

class TransactionRepository():
    def __init__(self, account_repo: AccountRepository, database):
        self.account_repo = account_repo
        self._transactions = database["Transaction"]

    def find_transactions(self): # CHANGE THIS SO ITS TAKING FROM ALL THE CUSTOMER'S ACCOUNTS
        transactions = self._transactions.find()
        return [Transaction(**txn) for txn in transactions]

    def find_transactions_by_account(self, account_id: str) -> List[Transaction]:
        transactions = self._transactions.find({"account_id": account_id})
        return [Transaction(**txn) for txn in transactions]

    def find_transactions_by_customer(self, customer_id: str) -> List[Transaction]:
        accounts = self.account_repo.find_accounts_by_customer(customer_id)
        account_ids = [account.account_id for account in accounts]

        transactions = self._transactions.find({"account_id": {"$in": account_ids}})
        return [Transaction(**txn) for txn in transactions]

    def transfer_money(self, account_id: str, transfer: Transaction) -> Optional[Transaction]:
        account = self.account_repo.find_by_id(account_id)

        if not account:
            return None

        dest_account = self.account_repo.find_by_id(transfer.dest_account_id)

        if not dest_account:
            return None

        if account.balance < transfer.amount:
            raise ValueError("Insufficient funds for transfer.")

        transfer.account_id = account_id

        transfer_data = transfer.model_dump(by_alias=True, exclude_none=True)
        result = self._transactions.insert_one(transfer_data)
        transfer.txn_id = str(result.inserted_id)

        self.account_repo.update_balance(account_id, -transfer.amount)
        self.account_repo.update_balance(transfer.dest_account_id, transfer.amount)
        return transfer

    def deposit_money(self, account_id: str, deposit: Transaction) -> Optional[Transaction]:
        account = self.account_repo.find_by_id(account_id)

        if not account:
            return None

        deposit.account_id = account_id

        deposit_data = deposit.model_dump(by_alias=True, exclude_none=True)
        result = self._transactions.insert_one(deposit_data)
        deposit.txn_id = str(result.inserted_id)

        self.account_repo.update_balance(account_id, deposit.amount)
        return deposit

    def withdraw_money(self, account_id: str, withdrawal: Transaction) -> Optional[Transaction]:
        account = self.account_repo.find_by_id(account_id)

        if not account:
            return None

        if account.balance < withdrawal.amount:
            raise ValueError("Insufficient funds for withdrawal.")

        withdrawal.account_id = account_id

        withdrawal_data = withdrawal.model_dump(by_alias=True, exclude_none=True)
        result = self._transactions.insert_one(withdrawal_data)
        withdrawal.txn_id = str(result.inserted_id)

        self.account_repo.update_balance(account_id, -withdrawal.amount)
        return withdrawal