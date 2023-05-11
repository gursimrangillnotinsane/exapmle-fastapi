from app.calculations import add
import pytest

@pytest.fixture
def zero_bankaccount():
    return BankAccount()

@pytest.fixture
def bankaccount():
    return BankAccount(50)
#pass them into argument



@pytest.mark.parametrize("num1, num2, ecpected",[
    (3,2,5),
    (7,1,8),
    (12,4,16)
    ])
def test_add(num1,num2,ecpected):
    print("test")
    assert add(num1,num2) ==ecpected












