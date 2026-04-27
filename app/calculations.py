
def add(num1: int, num2: int) -> int:
    return num1 + num2

def subtract(num1: int, num2: int) -> int:
    return num1 - num2

def multiply(num1: int, num2: int) -> int:
    return num1 * num2

def divide(num1: int, num2: int) -> float:
    return num1 / num2

## create exception class InsufficientFunds(Exception):

class InsufficientFunds(Exception): #custom exception class that inherits from the built-in Exception class. This allows us to raise this specific exception when there are insufficient funds in the bank account.
    pass

## create a dummy class called bank account for learning and testing purposes
class BankAccount():
    #contructor
    def __init__(self, starting_balance = 0):
        self.balance = starting_balance

    def deposit(self, amount):
        self.balance += amount

    def withdraw(self, amount):
        if self.balance < amount:
            raise InsufficientFunds("Insufficient funds")  #raises the InsufficientFunds exception with the message "Insufficient funds" if the balance is less than the amount to be withdrawn
        self.balance -= amount

    def collect_interest(self):
        self.balance *= 1.1
    