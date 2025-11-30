"""
Basic unit tests for Bank (pytest).
These tests create a temporary DB file by setting PYBANK_DB_PATH to a file in a tmp path.
"""
import os
import tempfile
import pytest
from bank import Bank




@pytest.fixture()
def bank_instance(tmp_path):
db_file = tmp_path / 'test.db'
os.environ['PYBANK_DB_PATH'] = str(db_file)
b = Bank()
yield b
b.close()




def test_create_and_get_account(bank_instance):
b = bank_instance
acc = b.create_account('TestUser', 100)
assert acc.id is not None
fetched = b.get_account(acc.id)
assert fetched is not None
assert fetched.name == 'TestUser'
assert abs(fetched.balance - 100.0) < 1e-6




def test_deposit_withdraw_transfer(bank_instance):
b = bank_instance
a1 = b.create_account('A1', 100)
a2 = b.create_account('A2', 50)


assert b.deposit(a1.id, 25) is True
fetched = b.get_account(a1.id)
assert abs(fetched.balance - 125.0) < 1e-6


assert b.withdraw(a1.id, 20) is True
fetched = b.get_account(a1.id)
assert abs(fetched.balance - 105.0) < 1e-6


assert b.transfer(a1.id, a2.id, 50) is True
fa = b.get_account(a1.id)
fb = b.get_account(a2.id)
assert abs(fa.balance - 55.0) < 1e-6
assert abs(fb.balance - 100.0) < 1e-6




def test_insufficient_funds(bank_instance):
b = bank_instance
a = b.create_account('Low', 10)
with pytest.raises(ValueError):
b.withdraw(a.id, 100)
