from models.Transaction import Transaction
from typing import Optional
from repositories.AccountRepository import AccountRepository

class TransactionRepository():
    def __init__(self, account_repo: AccountRepository):
        self.account_repo = account_repo 

    def transfer_money(self, account_id: int, transfer: Transaction) -> Optional[Transaction]:
        account = self.account_repo.find_by_id(account_id)

        if not account:
            return None

        transfer.account_id = account_id

        account.transactions.append(transfer)
        return transfer

    def deposit_money(self, account_id: int, deposit: Transaction) -> Optional[Transaction]:
        account = self.account_repo.find_by_id(account_id)

        if not account:
            return None

        deposit.account_id = account_id

        account.transactions.append(deposit)
        return deposit

    def withdraw_money(self, account_id: int, withdrawal: Transaction) -> Optional[Transaction]:
        account = self.account_repo.find_by_id(account_id)

        if not account:
            return None

        withdrawal.account_id = account_id

        account.transactions.append(withdrawal)
        return withdrawal