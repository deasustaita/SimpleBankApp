# consoleApp.py
# console app for a simple bank function

import random
import pdb

class Main:
    def __init__(self):
        self.customers = []

    @staticmethod
    def welcome_message():
        print("\nWelcome to The Bank.")
        print("1. Create an Account")
        print("2. Access an Account")
        print("3. Exit")

    def main(self):
        while True:
            self.welcome_message()
            choice = input("Select an option (1-3): ").strip()

            match choice:
                case "1":
                    self.create_account()
                case "2":
                    self.access_account()
                case "3":
                    print("\nThank you for banking with us. Goodbye.")
                    break
                case _:
                    print("\nInvalid choice. Please type a number between 1 and 3.")

    # username_exists: returns whether a username exists
    def username_exists(self, username):
        return any(customer.username.lower() == username.lower() for customer in self.customers)

    # _get_customer: returns a customer if it exists and nothing if it doesn't
    def _get_customer(self, username):
        for customer in self.customers:
            if customer.username.lower() == username.lower():
                return customer
        return None

    # create_account: creates a new customer account
    def create_account(self):
        print("\n--- Create Account ---")

        name = input("Enter full name: ").strip()
        if not name:
            print("\nName cannot be empty.")
            return

        username = input("Enter username: ").strip()
        if not username:
            print("\nUsername cannot be empty.")
            return
        if self.username_exists(username):
            print("\nError! That username is already taken. Try another.")
            return

        password = input("Enter password: ").strip()
        if not password:
            print("\nPassword cannot be empty.")
            return

        customer_id = self.generate_customer_id()

        new_customer = Customer(
            username=username,
            password=password,
            customer_id=customer_id,
            name=name,
        ) 

        # appends customers to a list so that they can be accessed at a later time
        self.customers.append(new_customer)

        print(
            f"\nThank you {name}, for making an account."
            f"\nYour username is {username}"
            f"\nYour customer ID is {customer_id}"
        )

    # generate_customer_id: generates a random, not taken customer_id
    def generate_customer_id(self):
        while True:
            customer_id = random.randint(1000, 9999)

            if not any(customer.customer_id == customer_id for customer in self.customers):
                return customer_id

    # access_account: log-in for existing users
    def access_account(self):
        print("\n--- Account Login ---")

        username = input("Enter username: ").strip()
        password = input("Enter password: ").strip()

        customer = self._get_customer(username)

        if not customer or customer.password != password:
            print("\nError: Invalid username or password.")
            return

        print(f"\nLogin successful. Welcome back, {customer.name}!")
        self.customer_menu(customer)

    # customer_menu: gives users choices on what they can do
    def customer_menu(self, customer):
        while True:
            print(f"\n--- {customer.name}'s Dashboard ---")
            print("1. View Accounts & Balances")
            print("2. Open a New Bank Account (Checking/Savings)")
            print("3. Deposit Funds")
            print("4. Withdraw Funds")
            print("5. Log Out")

            choice = input("Select an option (1-5): ").strip()

            match choice:
                case "1":
                    self.view_balances(customer)
                case "2":
                    self.open_bank_account(customer)
                case "3":
                    self.handle_deposit(customer)
                case "4":
                    self.handle_withdrawal(customer)
                case "5":
                    print("\nLogging out...")
                    break
                case _:
                    print("\nInvalid option. Please enter a number between 1 and 5.")

    # view_balances: shows the existing customer accounts
    def view_balances(self, customer):
        if not customer.accounts:
            print("\nYou currently don't have any open accounts.")
            return

        print('\n--- Your Accounts ---')

        for index, acc in enumerate(customer.accounts, 1):
            print(f'{index}. [{acc.account_type}] ID: {acc.account_id} | Balance: ${acc.balance:.2f}')

    # generate_account_id: generates a random non-existant account_id
    def generate_account_id(self):
        while True:
            account_id = random.randint(100000, 999999)

            account_exists = any(account.account_id == account_id for customer in self.customers for account in customer.accounts)

            if not account_exists:
                return account_id

    # open_bank_account: allows users to create a new checking or savings account
    def open_bank_account(self, customer):
        print("\n--- Open Bank Account ---")
        print("1. Checking Account")
        print("2. Savings Account")

        type_choice = input("Choice (1-2): ").strip()
        acc_id = self.generate_account_id()

        if type_choice not in ("1", "2"):
            print("\nInvalid choice. Returning to menu.")
            return

        if type_choice == "1":
            account = CheckingAccount(acc_id)
            account_type = "Checking Account"
        else:
            account = SavingsAccount(acc_id)
            account_type = "Savings Account"

        customer.accounts.append(account)

        print(
            f"\n{account_type} opened successfully!"
            f"\nYour account number is: {acc_id}"
            f"\nCurrent balance: ${account.balance:.2f}"
        )

    # handle_deposit: allows users to make a deposit to an account
    def handle_deposit(self, customer):
        acc = self.select_customer_account(customer)
        
        if not acc:
            return
        amount = self.get_amount("Enter deposit amount: $")

        if amount is None:
            return
        transaction_id = self.generate_transaction_id()
        deposit = Deposit(
            transaction_id,
            acc.account_id,
            amount
        )
        acc.balance += deposit.amount
        print(
            f"\nSuccessfully deposited ${amount:.2f}."
            f"\nAccount #: {acc.account_id}"
            f"\nNew Balance: ${acc.balance:.2f}"
        )

    # handle_withdrawal: allows users to make a withdrawal from an account
    def handle_withdrawal(self, customer):
        account = self.select_customer_account(customer)

        if account is None:
            return
        if account.balance < 0:
            print("Cannot withdraw from an overdrawn account.")
            return

        amount = self.get_amount("Enter withdrawal amount: $")

        if amount is None:
            return

        # savings accoutns do not overdraft
        if isinstance(account, SavingsAccount):
            if amount > account.balance:
                print(
                    f"\nTransaction Declined:"
                    f"\nSavings accounts do not allow overdrafts."
                    f"\nCurrent balance: ${account.balance:.2f}"
                )
                return

        transaction_id = self.generate_transaction_id()

        withdrawal = Withdrawal(
            transaction_id,
            account.account_id,
            amount
        )

        account.balance -= withdrawal.amount

        if account.balance < 0:
            print(
                f"\nWithdrawal complete."
                f"\nAccount #: {account.account_id}"
                f"\nNote: Account is overdrawn!"
                f"\nNew Balance: ${account.balance:.2f}"
            )
        else:
            print(
                f"\nSuccessfully withdrew ${amount:.2f}."
                f"\nAccount #: {account.account_id}"
                f"\nNew Balance: ${account.balance:.2f}"
            )

    # select_customer_account: allows the user to choose an account for withdrawal or deposits
    def select_customer_account(self, customer):
        if not customer.accounts:
            print(
                "\nYou must open an account "
                "before making transactions."
            )
            return None

        self.view_balances(customer)

        print("\nYou can select an account using:")
        print("1. The account list number")
        print("2. The full account number")

        selection = input("\nEnter selection: ").strip()

        # see if its a list position first
        if selection.isdigit():
            number = int(selection)

            if 1 <= number <= len(customer.accounts):
                return customer.accounts[number - 1]

            # if it isn't a list position try the account id
            account = self.get_account_by_id(customer, number)

            if account is not None:
                return account

        print("\nInvalid account selection.")
        return None

    def get_account_by_id(self, customer, account_id):
        for account in customer.accounts:
            if account.account_id == account_id:
                return account

        return None

    @staticmethod
    def get_amount(prompt):
        try:
            amount = float(input(prompt).strip())

            if amount <= 0:
                print("\nAmount must be greater than zero.")
                return None

            return amount

        except ValueError:
            print("\nInvalid input. Please enter a numerical value.")
            return None

    def generate_transaction_id(self):
        while True:
            transaction_id = random.randint(10000, 99999)

            transaction_exists = any(
                transaction_id == transaction.txn_id
                for customer in self.customers
                for account in customer.accounts
                for transaction in account.transactions
            )

            if not transaction_exists:
                return transaction_id

# Customer Class
class Customer:
    def __init__(self, username, password, customer_id, name, accounts=None):
        self.username = username
        self.password = password
        self.customer_id = customer_id
        self.name = name
        self.accounts = accounts if accounts is not None else []

# Account Classes
class Account:
    def __init__(self, account_id, balance=0.0):
        self.account_id = account_id
        self.balance = balance
        self.transactions = []

    def add_transaction(self, transaction):
        self.transactions.append(transaction)

class CheckingAccount(Account):
    # checking accounts allow overdrafts

    def __init__(self, account_id, balance=0.0):
        super().__init__(account_id, balance)
        self.account_type = "Checking Account"

class SavingsAccount(Account):
    # savings accounts do not allow overdrafts

    def __init__(self, account_id, balance=0.0):
        super().__init__(account_id, balance)
        self.account_type = "Savings Account"


# Transaction Classes
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


# Runs the program
if __name__ == "__main__":
    app = Main()
    app.main()