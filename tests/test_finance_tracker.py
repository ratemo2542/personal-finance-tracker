import tempfile
import unittest
from pathlib import Path
import main

class FinanceTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.old = main.DB_PATH
        main.DB_PATH = Path(self.tmp.name) / "test.db"

    def tearDown(self):
        main.DB_PATH = self.old
        self.tmp.cleanup()

    def test_income_expense_and_summary(self):
        main.add_transaction("income", 1000, "Allowance")
        main.add_transaction("expense", 250, "Food")
        with main.connect() as con:
            rows = con.execute("SELECT kind, amount FROM transactions").fetchall()
        self.assertEqual(len(rows), 2)
        self.assertEqual(sum(r["amount"] for r in rows if r["kind"] == "income"), 1000)
        self.assertEqual(sum(r["amount"] for r in rows if r["kind"] == "expense"), 250)

    def test_rejects_invalid_transaction(self):
        with self.assertRaises(ValueError):
            main.add_transaction("expense", 0, "Food")
        with self.assertRaises(ValueError):
            main.add_transaction("transfer", 10, "Other")

if __name__ == "__main__":
    unittest.main()
