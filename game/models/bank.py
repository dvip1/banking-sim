from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from typing import TYPE_CHECKING, Optional

from ..database import Base

if TYPE_CHECKING:
    from .empire import Empire
    from .currency import Currency
    from .balance import EmpireBalance


class Bank(Base):
    __tablename__ = "banks"

    id: Mapped[int] = mapped_column(primary_key=True)
    empire_id: Mapped[int] = mapped_column(ForeignKey("empires.id"), unique=True)

    empire: Mapped["Empire"] = relationship(back_populates="bank")

    def _get_balance(self, currency: "Currency") -> "EmpireBalance":
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

    def deposit(self, currency: "Currency", amount: float):
        if amount < 0:
            raise ValueError("Deposit amount must be positive")

        balance = self._get_balance(currency)
        balance.amount += amount
        return balance.amount

    def withdraw(self, currency: "Currency", amount: float):
        if amount < 0:
            raise ValueError("Withdraw amount must be positive")

        balance = self._get_balance(currency)

        if balance.amount < amount:
            raise ValueError("Insufficient funds")

        balance.amount -= amount
        return balance.amount
    
    def list_currencies(self):
        return self.empire.currencies
    
    def get_balance(self, currency: "Currency") -> float:
        return self._get_balance(currency).amount
    