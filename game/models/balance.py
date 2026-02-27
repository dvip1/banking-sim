from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from typing import TYPE_CHECKING
from ..services.currency_service import CurrencyService

from ..database import Base

if TYPE_CHECKING:
    from .empire import Empire
    from .currency import Currency

class EmpireBalance(Base):
    __tablename__ = "empire_balances"

    empire_id: Mapped[int] = mapped_column(ForeignKey("empires.id"), primary_key=True)
    currency_id: Mapped[int] = mapped_column(ForeignKey("currencies.id"), primary_key=True)
    amount: Mapped[float] = mapped_column(default=0.0)
    domestic_wealth: Mapped[float] = mapped_column(default=0.0)
    empire: Mapped["Empire"] = relationship(back_populates="balances")
    currency: Mapped["Currency"] = relationship()

    def __repr__(self):
        return f"<EmpireBalance(empire={self.empire_id}, currency={self.currency_id}, amount={self.amount}, domestic_wealth={self.domestic_wealth})>"
    
      

