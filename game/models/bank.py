from sqlalchemy.orm import Mapped, mapped_column, relationship, Session
from sqlalchemy import ForeignKey
from typing import TYPE_CHECKING, Optional, ClassVar

from ..database import Base

if TYPE_CHECKING:
    from .empire import Empire
    from .currency import Currency
    from .balance import EmpireBalance
    from ..services.currency_service import CurrencyService


class Bank(Base):
    __tablename__ = "banks"

    id: Mapped[int] = mapped_column(primary_key=True)
    empire_id: Mapped[int] = mapped_column(ForeignKey("empires.id"), unique=True)
    empire: Mapped["Empire"] = relationship(back_populates="bank")
    _session: ClassVar[Optional[Session]] = None

    def __init__(
        self,
        empire_id: Optional[int] = None,
        empire: Optional["Empire"] = None,
        session: Optional[Session] = None,
    ):
        if empire is not None:
            self.empire = empire
            if empire.id is not None:
                self.empire_id = empire.id
        elif empire_id is not None:
            self.empire_id = empire_id
        self._session = session

    def _resolve_currency(self, currency: Optional["Currency"], session: Optional[Session]) -> "Currency":
        if currency is not None:
            return currency
        if session is None:
            raise ValueError("Session is required when currency is not provided")

        from ..services.currency_service import CurrencyService
        baseline = CurrencyService.ensure_baseline_exists(session)
        if baseline is None:
            raise ValueError("Baseline currency is required")
        return baseline

    def _get_balance(self, currency: Optional["Currency"], session: Optional[Session]) -> "EmpireBalance":
        resolved_session = session or getattr(self, "_session", None)
        currency = self._resolve_currency(currency, resolved_session)
        for balance in self.empire.balances:
            if balance.currency_id == currency.id:
                return balance

        from .balance import EmpireBalance
        new_balance = EmpireBalance(
            empire=self.empire,
            currency=currency,
            amount=0
        )
        self.empire.balances.append(new_balance)
        return new_balance

    def deposit(self, currency: Optional["Currency"], amount: float, session: Optional[Session] = None):
        if amount < 0:
            raise ValueError("Deposit amount must be positive")

        balance = self._get_balance(currency, session)
        balance.amount += amount
        return balance.amount

    def withdraw(self, currency: Optional["Currency"], amount: float, session: Optional[Session] = None):
        if amount < 0:
            raise ValueError("Withdraw amount must be positive")

        balance = self._get_balance(currency, session)

        if balance.amount < amount:
            raise ValueError("Insufficient funds")

        balance.amount -= amount
        return balance.amount
    
    def list_currencies(self, session: Optional[Session] = None, include_baseline: bool = True):
        currencies = list(self.empire.currencies)
        resolved_session = session or self._session
        if include_baseline and resolved_session is not None:
            from ..services.currency_service import CurrencyService
            baseline = CurrencyService.get_baseline_currency(resolved_session)
            if baseline is not None and baseline not in currencies:
                currencies.append(baseline)
        return currencies
    
    def get_balance(self, currency: Optional["Currency"], session: Optional[Session] = None) -> float:
        return self._get_balance(currency, session).amount    
    