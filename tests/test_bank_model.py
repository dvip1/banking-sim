
import unittest
import sys
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from game.database import Base
from game.models.empire import Empire
from game.models.currency import Currency
from game.models.bank import Bank
from game.services.currency_service import CurrencyService

class TestBankModel(unittest.TestCase):
    def setUp(self):
        self.engine = create_engine("sqlite:///:memory:")
        Base.metadata.create_all(self.engine)
        self.session = Session(self.engine)

    def tearDown(self):
        self.session.close()

    def test_bank_operations(self):
        print("\n--- Testing Bank Operations ---")
        
        # Setup
        currency = Currency(name="Gold", symbol="G", is_baseline=True, exchange_rate=1.0)
        self.session.add(currency)
        
        empire = Empire(name="Banking Empire", game_id=1)
        self.session.add(empire)
        self.session.commit()

        # Create Bank
        bank = Bank(empire=empire, session=self.session)
        self.session.add(bank)
        self.session.commit()
        
        self.assertIsNotNone(empire.bank)
        print("Bank created and linked to Empire.")

        # Deposit (no currency specified -> baseline)
        bank.deposit(None, 100.0)
        self.assertEqual(bank.get_balance(None), 100.0)
        print("Deposited 100.0 Gold.")

        # Withdraw (no currency specified -> baseline)
        bank.withdraw(None, 50.0)
        self.assertEqual(bank.get_balance(None), 50.0)
        print("Withdrew 50.0 Gold.")

        # Overdraft Check
        with self.assertRaises(ValueError):
            bank.withdraw(None, 100.0)
        print("Overdraft (withdraw 100 from 50) correctly raised ValueError.")

        # Verify Balance persistence
        self.session.commit()
        self.session.refresh(empire)
        self.assertEqual(empire.balances[0].amount, 50.0)
        print("Balance persisted in Empire balances.")

if __name__ == '__main__':
    unittest.main()
