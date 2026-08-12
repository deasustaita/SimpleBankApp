from models.Transaction import Transaction
from repositories.TransactionRepository import TransactionRepository
from typing import Optional, List

class TransactionService():
    def __init__(self, repository: TransactionRepository):
        self.repository = repository

    def transfer_money(self, account_id: int, transaction: Transaction) -> Optional[Transaction]:
        return self.repository.transfer_money(account_id, transaction)

    def deposit_money(self, account_id: int, transaction: Transaction) -> Optional[Transaction]:
        return self.repository.deposit_money(account_id, transaction)

    def withdraw_money(self, account_id: int, transaction: Transaction) -> Optional[Transaction]:
        return self.repository.withdraw_money(account_id, transaction)

    def get_transactions(self) -> List[Transaction]:
        return self.repository.find_transactions()