# consoleApp.py
# console app for a simple bank function

import random


class Main:
    def __init__(self):
        self.customers = []
        self.transactions = []

    @staticmethod
    def welcome_message():
        print("Welcome to The Bank.")
        print("1. Create an Account")
        print("2. View Account Details")
        print("3. Deposit Money")
        print("4. Withdraw Money")
        print("5. View Transaction History")
        print("6. Exit")

    def main(self):
        while True:
            self.welcome_message()
            choice = input("Select an option (1-6): ").strip()

            match choice:
                case "1":
                    self.create_account()
                case "2":
                    self.view_account_details()
                case "3":
                    self.deposit_money()
                case "4":
                    self.withdraw_money()
                case "5":
                    self.view_transaction_history()
                case "6":
                    print("\nThank you for banking with us. Goodbye.")
                    break
                case _:
                    print("\nInvalid choice. Please type a number between 1 and 6.")

    def create_account(self):
        name = input("Enter full name: ").strip()
        usnm = input("Enter username: ").strip()
        pswd = input("Enter password: ").strip()

        account_type = input("Account type? (1 for Checking, 2 for Savings): ").strip()
        account_id = f"ACC - {random.randint(1000,9999)}"

        if account_id == "2":
            acc = SavingsAccount(account_id)
        else:
            acc = CheckingAccount(account_id)

        customer_id = f'CUST-{random.randint(100, 999)}'
        new_customer = Customer(
            username=usnm,
            password = pswd,
            id = customer_id,
            name=name,
            accounts=[acc],
        )

        self.customers.append(new_customer)
        print(f"Account created successfully! Your Account ID is '{acc.account_id}' under Customer ID '{customer_id}'")

    def view_account_details(self):
        print("\n--- View Account Details ---")
        acc_id = input("Enter Account ID: ").strip()
        customer, acc = self._find_customer_and_account(acc_id)

        if acc:
            print(f"\nCustomer Name: {customer.name}")
            print(f"Customer ID:   {customer.id}")
            print(f"Account ID:    {acc.account_id}")
            print(f"Type:          {acc.accountType}")
            print(f"Balance:       ${acc.balance:.2f}")
        else:
            print("Account not found.")

    def deposit_money(self):
        print("\n--- Deposit Money ---")
        acc_id = input("Enter Account ID: ").strip()
        _, acc = self._find_customer_and_account(acc_id)

        if not acc:
            print("Account not found.")
            return

        try:
            amount = float(input("Enter deposit amount: $"))
            if amount <= 0:
                print("Deposit amount must be positive.")
                return

            acc.balance += amount
            txn_id = f"TXN-{random.randint(10000, 99999)}"
            txn = Deposit(txn_id, acc.account_id, amount)
            self.transactions.append(txn)

            print(f"Successfully deposited ${amount:.2f}. New Balance: ${acc.balance:.2f}")
        except ValueError:
            print("Invalid input. Amount must be a number.")

    def withdraw_money(self):
        print("\n--- Withdraw Money ---")
        acc_id = input("Enter Account ID: ").strip()
        _, acc = self._find_customer_and_account(acc_id)

        if not acc:
            print("Account not found.")
            return

        try:
            amount = float(input("Enter withdrawal amount: $"))
            if amount <= 0:
                print("Withdrawal amount must be positive.")
                return

            if amount > acc.balance:
                print(f"Insufficient funds! Current balance: ${acc.balance:.2f}")
                return

            acc.balance -= amount
            txn_id = f"TXN-{random.randint(10000, 99999)}"
            txn = Withdrawal(txn_id, acc.account_id, amount)
            self.transactions.append(txn)

            print(f"Successfully withdrew ${amount:.2f}. Remaining Balance: ${acc.balance:.2f}")
        except ValueError:
            print("Invalid input. Amount must be a number.")

    def view_transaction_history(self):
        print("\n--- Transaction History ---")
        acc_id = input("Enter Account ID: ").strip()

        acc_txns = [t for t in self.transactions if t.account_id == acc_id]

        if not acc_txns:
            print("No transactions found for this account ID.")
            return

        print(f"\nTransactions for Account '{acc_id}':")
        for t in acc_txns:
            sign = "+" if t.txn_type == "Deposit" else "-"
            print(f"  [{t.txn_id}] {t.txn_type}: {sign}${t.amount:.2f}")


class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password

class Customer(User):
    def __init__(self, username, password, id, name, accounts=None):
        super().__init__(username, password)
        self.id = id
        self.name = name
        self.accounts = accounts if accounts is not None else []

class Account:
    def __init__(self, account_id, balance=0):
        self.account_id = account_id
        self.balance = balance

class CheckingAccount(Account):
    def __init__(self, account_id, balance=0):
        super().__init__(account_id, balance)
        self.accountType = "Checking Account"

class SavingsAccount(Account):
    def __init__(self, account_id, balance=0):
        super().__init__(account_id, balance)
        self.accountType = "Savings Account"

class Transaction:
    def __init__(self, txn_id, account_id, amount):
        self.txn_id = txn_id
        self.account_id = account_id
        self.amount = amount

class Deposit(Transaction):
    def __init__(self, txn_id, account_id, amount):
        super().__init__(txn_id, account_id, amount)
        self.txn_type = "Deposit"

class Withdrawal(Transaction):
    def __init__(self, txn_id, account_id, amount):
        super().__init__(txn_id, account_id, amount)
        self.txn_type = "Withdrawal"

if __name__ == "__main__":
    app = Main()
    app.main()