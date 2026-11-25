# Personal Finance Tracker

A local-first command-line finance tracker built with Python and SQLite. Record income and expenses, inspect transactions, and generate category summaries without sending financial data to a third-party service.

## Features
- Add income and expense transactions with date, category, amount, and note
- List recent transactions
- Show current balance and totals
- Summarize expenses by category
- Persistent local SQLite database

## Requirements
- Python 3.10+
- No third-party packages

## Run
```bash
python main.py add --kind expense --amount 450 --category food --note "Lunch"
python main.py add --kind income --amount 15000 --category allowance
python main.py list
python main.py summary
```

The database is created automatically at `finance.db` in the current directory. Keep it private and back it up. Amounts must be positive numbers; use one currency consistently.

## Project structure
- `main.py` — CLI and database operations
- `tests/test_finance.py` — automated tests

## Safety
This is a personal record-keeping tool, not financial advice or a banking application.
