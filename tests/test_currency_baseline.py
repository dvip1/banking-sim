
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
from game.models.balance import EmpireBalance
from game.services.currency_service import CurrencyService

class TestBaselineCurrency(unittest.TestCase):
    def setUp(self):
        # Use in-memory SQLite database for testing
        self.engine = create_engine("sqlite:///:memory:")
        Base.metadata.create_all(self.engine)
        self.session = Session(self.engine)

    def tearDown(self):
        self.session.close()

    def test_baseline_currency_logic(self):
        print("\n--- Testing Baseline Currency Logic ---")
        
        # 1. Create Baseline Currency
        baseline = CurrencyService.ensure_baseline_exists(self.session, name="Gold Standard", symbol="GS")
        self.assertTrue(baseline.is_baseline)
        self.assertEqual(baseline.exchange_rate, 1.0)
        print(f"Created Baseline: {baseline.name}, Rate: {baseline.exchange_rate}")

        # 2. Create Secondary Currency
        fiat = Currency(name="Fiat USD", symbol="$")
        fiat.is_baseline = False
        fiat.exchange_rate = 0.5 # Worth half of baseline
        self.session.add(fiat)
        self.session.commit()
        print(f"Created Secondary: {fiat.name}, Rate: {fiat.exchange_rate}")

        # 3. Create Empire
        empire = Empire(name="Test Empire", game_id=1)
        self.session.add(empire)
        self.session.commit()

        # 4. Add Balances
        # 100 Baseline -> Worth 100
        # 200 Fiat -> Worth 200 * 0.5 = 100
        # Total Wealth should be 200
        
        bal1 = EmpireBalance(empire_id=empire.id, currency_id=baseline.id, amount=100)
        bal2 = EmpireBalance(empire_id=empire.id, currency_id=fiat.id, amount=200)
        
        self.session.add_all([bal1, bal2])
        self.session.commit()
        
        # Refresh empire to load balances
        self.session.refresh(empire)
        
        print(f"Empire Balances: {[b.amount for b in empire.balances]}")
        print(f"Calculated Total Wealth (Baseline): {empire.total_wealth}")

        self.assertEqual(empire.total_wealth, 200.0)
        print("SUCCESS: Total wealth calculation matches expected value.")

    def test_currency_conversion(self):
        print("\n--- Testing Currency Conversion ---")
        baseline = CurrencyService.ensure_baseline_exists(self.session)
        euro = Currency(name="Euro", symbol="E")
        euro.exchange_rate = 0.8 
        self.session.add(euro)
        self.session.commit()

        # Convert 100 Euro to Baseline
        # 100 * 0.8 = 80 Baseline
        converted = CurrencyService.convert(100, euro, baseline)
        self.assertEqual(converted, 80.0)
        print(f"100 Euro (0.8) -> {converted} Baseline")

        # Convert 80 Baseline to Euro
        # 80 / 0.8 = 100 Euro
        converted_back = CurrencyService.convert(80, baseline, euro)
        self.assertEqual(converted_back, 100.0)
        print(f"80 Baseline -> {converted_back} Euro")

if __name__ == '__main__':
    unittest.main()
