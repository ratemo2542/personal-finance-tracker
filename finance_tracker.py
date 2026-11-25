"""Local-first personal finance tracker."""
from __future__ import annotations
import csv
import json
from datetime import date
from pathlib import Path

DATA_FILE = Path("finance_data.json")

def load_transactions(path: Path = DATA_FILE) -> list[dict]:
    if not path.exists():
        return []
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as exc:
        raise ValueError(f"Could not read {path}: {exc}") from exc
    if not isinstance(data, list):
        raise ValueError("Finance data must be a JSON list.")
    return data

def save_transactions(items: list[dict], path: Path = DATA_FILE) -> None:
    path.write_text(json.dumps(items, indent=2), encoding="utf-8")

def add_transaction(items: list[dict], kind: str, amount: float, category: str, note: str = "", day: str | None = None) -> dict:
    if kind not in {"income", "expense"}:
        raise ValueError("kind must be income or expense")
    if amount <= 0:
        raise ValueError("amount must be greater than zero")
    parsed_day = date.fromisoformat(day) if day else date.today()
    item = {"id": len(items) + 1, "date": parsed_day.isoformat(), "type": kind,
            "amount": round(float(amount), 2), "category": category.strip() or "Uncategorized",
            "note": note.strip()}
    items.append(item)
    return item

def summary(items: list[dict]) -> dict:
    income = sum(float(x["amount"]) for x in items if x["type"] == "income")
    expenses = sum(float(x["amount"]) for x in items if x["type"] == "expense")
    by_category: dict[str, float] = {}
    for item in items:
        if item["type"] == "expense":
            cat = item.get("category", "Uncategorized")
            by_category[cat] = by_category.get(cat, 0.0) + float(item["amount"])
    return {"income": round(income, 2), "expenses": round(expenses, 2),
            "balance": round(income - expenses, 2), "spending_by_category": by_category}

def export_csv(items: list[dict], destination: Path) -> None:
    fields = ["id", "date", "type", "amount", "category", "note"]
    with destination.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(items)

def main() -> None:
    items = load_transactions()
    while True:
        print("\nPERSONAL FINANCE TRACKER\n1. Add income\n2. Add expense\n3. List transactions\n4. Summary\n5. Export CSV\n0. Exit")
        choice = input("Choose: ").strip()
        try:
            if choice in {"1", "2"}:
                amount = float(input("Amount: "))
                category = input("Category: ")
                note = input("Note (optional): ")
                add_transaction(items, "income" if choice == "1" else "expense", amount, category, note)
                save_transactions(items)
                print("Transaction saved.")
            elif choice == "3":
                for item in items:
                    print(f'{item["date"]} | {item["type"]:7} | {item["amount"]:10.2f} | {item["category"]} | {item["note"]}')
            elif choice == "4":
                totals = summary(items)
                print(f'Income: {totals["income"]:.2f}\nExpenses: {totals["expenses"]:.2f}\nBalance: {totals["balance"]:.2f}')
                for category, amount in sorted(totals["spending_by_category"].items()):
                    print(f"  {category}: {amount:.2f}")
            elif choice == "5":
                export_csv(items, Path("transactions.csv"))
                print("Exported to transactions.csv")
            elif choice == "0":
                break
            else:
                print("Unknown option.")
        except (ValueError, OSError) as exc:
            print(f"Error: {exc}")

if __name__ == "__main__":
    main()
