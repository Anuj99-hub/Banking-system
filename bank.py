def withdraw(self, account_id: int, amount: float, note: Optional[str] = None) -> bool:
if amount <= 0:
raise ValueError('Withdraw amount must be positive')
cur = self.conn.cursor()
# check balance
cur.execute('SELECT balance FROM accounts WHERE id = ?', (account_id,))
row = cur.fetchone()
if not row:
return False
if row['balance'] < amount:
raise ValueError('Insufficient funds')
cur.execute('UPDATE accounts SET balance = balance - ? WHERE id = ?', (amount, account_id))
self._record_transaction(account_id, 'withdraw', amount, note)
return True


def transfer(self, from_id: int, to_id: int, amount: float, note: Optional[str] = None) -> bool:
if amount <= 0:
raise ValueError('Transfer amount must be positive')
cur = self.conn.cursor()
# ensure both accounts exist
cur.execute('SELECT balance FROM accounts WHERE id = ?', (from_id,))
row_from = cur.fetchone()
cur.execute('SELECT id FROM accounts WHERE id = ?', (to_id,))
row_to = cur.fetchone()
if not row_from or not row_to:
return False
if row_from['balance'] < amount:
raise ValueError('Insufficient funds')
# perform transfer inside a transaction
try:
cur.execute('UPDATE accounts SET balance = balance - ? WHERE id = ?', (amount, from_id))
cur.execute('UPDATE accounts SET balance = balance + ? WHERE id = ?', (amount, to_id))
now = datetime.utcnow().isoformat()
cur.execute('INSERT INTO transactions (account_id, type, amount, timestamp, note, related_account) VALUES (?, ?, ?, ?, ?, ?)',
(from_id, 'transfer_out', amount, now, note, to_id))
cur.execute('INSERT INTO transactions (account_id, type, amount, timestamp, note, related_account) VALUES (?, ?, ?, ?, ?, ?)',
(to_id, 'transfer_in', amount, now, note, from_id))
self.conn.commit()
return True
except Exception:
self.conn.rollback()
raise


def get_transactions(self, account_id: int, limit: int = 100) -> List[Tuple]:
cur = self.conn.cursor()
cur.execute('SELECT * FROM transactions WHERE account_id = ? ORDER BY id DESC LIMIT ?', (account_id, limit))
rows = cur.fetchall()
return [dict(r) for r in rows]


def close(self):
try:
self.conn.close()
except Exception:
pass




if __name__ == '__main__':
# quick manual test (safe: create and print a demo account)
b = Bank()
a = b.create_account('Alice', 100)
b.deposit(a.id, 50, 'pay in')
print(b.get_account(a.id))
