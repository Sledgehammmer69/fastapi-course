import pytest
from app.calculations import add, subtract, multiply, divide, BankAccount, InsufficientFunds

@pytest.fixture             #defines a fixture that can be used in test functions
def zero_bank_account():
    print("creating empty bank account")
    return BankAccount()    #returns a new instance of BankAccount with the default balance (0) when the fixture is used in a test function

@pytest.fixture
def bank_account():
    return BankAccount(50)  #returns a new instance of BankAccount with an initial balance of 50 when the fixture is used in a test function

@pytest.mark.parametrize("num1, num2, expected", [
    (3, 5, 8),
    (10, 2, 12),
    (12, 4, 16)
])
def test_add(num1, num2, expected):
    print("Testing add function")
    assert add(num1, num2) == expected

def test_subtract():
    print("Testing subtract function")
    assert subtract(10, 5) == 5

def test_multiply():
    print("Testing multiply function")
    assert multiply(4, 5) == 20

def test_divide():
    print("Testing divide function")
    assert divide(10, 5) == 2


# BankAccount tests

def test_bank_set_initial_amount(bank_account):    #uses the bank_account fixture to create a new BankAccount instance with an initial balance of 50 and checks if the balance is indeed 50
    assert bank_account.balance == 50 

def test_bank_default_amount(zero_bank_account):    #uses the zero_bank_account fixture to create a new BankAccount instance with the default balance (0) and checks if the balance is indeed 0
    print("testing my bank account")
    assert zero_bank_account.balance == 0

def test_withdraw(bank_account):
    bank_account.withdraw(10)
    assert bank_account.balance == 40

def test_deposit(bank_account):
    bank_account.deposit(200)
    assert bank_account.balance == 250

def test_collect_interest(bank_account):
    bank_account.collect_interest()
    assert round(bank_account.balance, 6) == 55 # rounding to 6 decimal places to avoid floating point precision issues



@pytest.mark.parametrize("deposited, withdrawn, expected", [
    (200, 100, 100),
    (50, 10, 40),
    (1200, 200, 1000)
])
#we can do all 3 tests here...start with 0, deposit 200 then withdraw 100...we can use parametrize and 
#fixture together...

def test_bank_transaction(zero_bank_account, deposited, withdrawn, expected):
    zero_bank_account.deposit(deposited)
    zero_bank_account.withdraw(withdrawn)
    assert zero_bank_account.balance == expected

def test_insufficient_funds(bank_account):
    with pytest.raises(InsufficientFunds):  #expects the InsufficientFunds exception to be raised when the code inside the with block is executed. If the exception is not raised, the test will fail.
        bank_account.withdraw(200)  # Attempt to withdraw more than the current balance
