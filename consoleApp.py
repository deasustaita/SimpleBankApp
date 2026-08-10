# consoleApp.py
# console app for a simple bank function

import argparse


class Main:
    def welcome_message():
            print("Welcome to The Bank.")

    def main():
        pass

    


class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password

class Customer(User):
    def __init__(self, username, password, id, name, accounts):
        super().__init__(username, password)
        self.id = id
        self.name = name
        self.accounts = accounts

    def getID(self):
        return self.id
    def setID(self, id):
        self.id = id
    def getName(self):
        return self.name
    def setName(self, name):
        self.name = name
    def getAccounts(self):
        return self.accounts
    def setAccounts(self, accounts):
        self.accounts = accounts

class Account:
    def __init__(self, accountID, balance):
        self.accountID = accountID
        self.balance = balance

    def getAccountID(self):
        return self.accountID
    def setAccountID(self, accountID):
        self.accountID = accountID
    def getBalance(self):
        return self.balance
    def setBalance(self, balance):
        self.balance = balance

class Transaction:
    pass