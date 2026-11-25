"""Personal Finance Tracker: a small local-first SQLite CLI."""
import argparse
import sqlite3
from datetime import date
from pathlib import Path

DB_PATH = Path(__file__).with_name("finance.db")

def connect():
    con = sqlite3.connect(DB_PATH)
    con.row_factory = sqlite3.Row
    con.execute("""CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        kind TEXT NOT NULL CHECK(kind IN ('income','expense')),
        amount REAL NOT NULL CHECK(amount > 0),
        category TEXT NOT NULL,
        note TEXT NOT NULL DEFAULT '',
        happened_on TEXT NOT NULL
    )""")
    return con

def add_transaction(kind, amount, category, note="", happened_on=None):
    if kind not in {"income", "expense"} or amount <= 0 or not category.strip():
        raise ValueError("Use income/expense, a positive amount, and a category.")
    with connect() as con:
        cur = con.execute(
            "INSERT INTO transactions(kind,amount,category,note,happened_on) VALUES(?,?,?,?,?)",
            (kind, amount, category.strip(), note.strip(), happened_on or date.today().isoformat()))
        return cur.lastrowid

def summary():
    with connect() as con:
        rows = con.execute("SELECT kind, SUM(amount) total FROM transactions GROUP BY kind").fetchall()
        totals = {r["kind"]: r["total"] or 0 for r in rows}
        categories = con.execute(
            "SELECT category, SUM(amount) total FROM transactions WHERE kind='expense' GROUP BY category ORDER BY total DESC"
        ).fetchall()
    income, expenses = totals.get("income", 0), totals.get("expense", 0)
    print(f"Income:   {income:,.2f}\nExpenses: {expenses:,.2f}\nBalance:  {income-expenses:,.2f}")
    if categories:
        print("\nExpenses by category:")
        for row in categories:
            print(f"  {row['category']:<20} {row['total']:>12,.2f}")

def main():
    parser = argparse.ArgumentParser(description="Track income and expenses locally.")
    sub = parser.add_subparsers(dest="command", required=True)
    add = sub.add_parser("add", help="record a transaction")
    add.add_argument("--kind", choices=["income", "expense"], required=True)
    add.add_argument("--amount", type=float, required=True)
    add.add_argument("--category", required=True)
    add.add_argument("--note", default="")
    add.add_argument("--date", dest="happened_on", help="YYYY-MM-DD (defaults to today)")
    sub.add_parser("list", help="show transactions")
    sub.add_parser("summary", help="show totals and spending by category")
    args = parser.parse_args()
    if args.command == "add":
        try:
            ident = add_transaction(args.kind, args.amount, args.category, args.note, args.happened_on)
            print(f"Saved transaction #{ident}.")
        except ValueError as exc:
            parser.error(str(exc))
    elif args.command == "list":
        with connect() as con:
            rows = con.execute("SELECT * FROM transactions ORDER BY happened_on DESC, id DESC").fetchall()
        if not rows:
            print("No transactions yet.")
        for r in rows:
            print(f"#{r['id']} {r['happened_on']} {r['kind']:<7} {r['amount']:>10,.2f}  {r['category']}  {r['note']}")
    else:
        summary()

if __name__ == "__main__":
    main()
