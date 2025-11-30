import os
p_transfer.add_argument('amount', type=float)


# balance
p_balance = sub.add_parser('balance')
p_balance.add_argument('account_id', type=int)


# statement
p_statement = sub.add_parser('statement')
p_statement.add_argument('account_id', type=int)
p_statement.add_argument('--limit', type=int, default=50)


args = parser.parse_args(argv)


bank = Bank()


try:
if args.cmd == 'create':
acc = bank.create_account(args.name, args.initial)
if RICH_AVAILABLE and _console is not None:
_console.print(f"Created account {acc.name} with id {acc.id} and balance {acc.balance:.2f}")
else:
print(f"Created account {acc.name} with id {acc.id} and balance {acc.balance:.2f}")


elif args.cmd == 'list':
accounts = bank.list_accounts()
rows = [{'id': a.id, 'name': a.name, 'balance': f"{a.balance:.2f}", 'created_at': a.created_at} for a in accounts]
print_table(rows, ['id', 'name', 'balance', 'created_at'])


elif args.cmd == 'deposit':
bank.deposit(args.account_id, args.amount)
print(f"Deposited {args.amount:.2f} to account {args.account_id}")


elif args.cmd == 'withdraw':
bank.withdraw(args.account_id, args.amount)
print(f"Withdrew {args.amount:.2f} from account {args.account_id}")


elif args.cmd == 'transfer':
bank.transfer(args.from_id, args.to_id, args.amount)
print(f"Transferred {args.amount:.2f} from {args.from_id} to {args.to_id}")


elif args.cmd == 'balance':
acc = bank.get_account(args.account_id)
if not acc:
print(f"Account {args.account_id} not found")
else:
print(f"Account {acc.name} ({acc.id}) balance: {acc.balance:.2f}")


elif args.cmd == 'statement':
txns = bank.get_transactions(args.account_id, args.limit)
# normalize rows
rows = [{
'id': t['id'], 'type': t['type'], 'amount': f"{t['amount']:.2f}",
'timestamp': t['timestamp'], 'note': t.get('note') or '', 'related': t.get('related_account') or ''
} for t in txns]
print_table(rows, ['id', 'type', 'amount', 'timestamp', 'note', 'related'])


else:
parser.print_help()
except Exception as e:
print(f"Error: {e}")
finally:
bank.close()




if __name__ == '__main__':
main()
