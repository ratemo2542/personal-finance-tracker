import tempfile
import unittest
from pathlib import Path
from finance_tracker import add_transaction, summary, save_transactions, load_transactions

class FinanceTrackerTests(unittest.TestCase):
    def test_add_and_summarize(self):
        items = []
        add_transaction(items, "income", 1000, "Allowance")
        add_transaction(items, "expense", 250, "Food")
        result = summary(items)
        self.assertEqual(result["income"], 1000)
        self.assertEqual(result["expenses"], 250)
        self.assertEqual(result["balance"], 750)
        self.assertEqual(result["spending_by_category"]["Food"], 250)

    def test_reject_invalid_amount(self):
        with self.assertRaises(ValueError):
            add_transaction([], "expense", 0, "Food")

    def test_persistence(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "data.json"
            save_transactions([{"type":"income","amount":5}], path)
            self.assertEqual(load_transactions(path)[0]["amount"], 5)

if __name__ == "__main__":
    unittest.main()
