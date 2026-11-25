import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import main

class FinanceTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.db = Path(self.tmp.name) / "test.db"
        self.patch = patch.object(main, "DB_PATH", self.db)
        self.patch.start()
    def tearDown(self):
        self.patch.stop()
        self.tmp.cleanup()
    def test_add_and_persist(self):
        ident = main.add_transaction("income", 1000, "allowance")
        self.assertEqual(ident, 1)
        with main.connect() as con:
            row = con.execute("SELECT amount, kind FROM transactions").fetchone()
        self.assertEqual((row["amount"], row["kind"]), (1000, "income"))
    def test_reject_invalid_amount(self):
        with self.assertRaises(ValueError):
            main.add_transaction("expense", 0, "food")
if __name__ == "__main__":
    unittest.main()
