from sqlalchemy.orm import Session
from sqlalchemy import select
from typing import TYPE_CHECKING
from ..models.currency import Currency

if TYPE_CHECKING:
    from ..models.empire import Empire

class CurrencyService:
    @staticmethod
    def get_baseline_currency(session: Session) -> Currency | None:
        """Retrieves the baseline currency."""
        stmt = select(Currency).where(Currency.is_baseline == True)
        return session.execute(stmt).scalar_one_or_none()

    @staticmethod
    def ensure_baseline_exists(session: Session, name="Global Standard", symbol="GS", empire_id=None):
        """Ensures a baseline currency exists. Creates one if not."""
        currency = CurrencyService.get_baseline_currency(session)
        if not currency:
            currency = Currency(name=name, symbol=symbol, empire_id=empire_id)
            currency.is_baseline = True
            currency.exchange_rate = 1.0
            session.add(currency)
            session.commit()
            session.refresh(currency)
        return currency

    @staticmethod
    def convert(amount: float, from_currency: Currency, to_currency: Currency) -> float:
        """
        Converts an amount from one currency to another using their exchange rates.
        Formula: (Amount * FromRate) / ToRate
        """
        if from_currency.id == to_currency.id:
            return amount
        
        # Convert to baseline value first (Amount * Rate)
        baseline_value = amount * from_currency.exchange_rate
        
        # Convert baseline value to target currency (Value / TargetRate)
        return baseline_value / to_currency.exchange_rate

    @staticmethod
    def per_capita_all_currencies(empire: "Empire") -> float:
        """
        Calculates the per capita wealth of an empire across all its currencies,
        using the DOMESTIC wealth (population's money).
        """
        if empire.population <= 0:
            return 0.0
            
        total_wealth = 0
        for balance in empire.balances:
            total_wealth += balance.domestic_wealth * balance.currency.exchange_rate
        return total_wealth / empire.population

    @staticmethod
    def per_capita_currency(empire: "Empire", currency: Currency) -> float:
        """
        Calculates the per capita wealth of an empire in a specific currency,
        using the DOMESTIC wealth (population's money).
        """
        if empire.population <= 0:
            return 0.0
            
        for balance in empire.balances:
            if balance.currency_id == currency.id:
                # Changed from balance.amount to balance.domestic_wealth
                return (balance.domestic_wealth * balance.currency.exchange_rate) / empire.population
        return 0.0