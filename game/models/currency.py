from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from typing import Optional, TYPE_CHECKING
from ..database import Base

if TYPE_CHECKING:
    from .empire import Empire

class Currency(Base):
    __tablename__ = "currencies"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    empire_id: Mapped[Optional[int]] = mapped_column(ForeignKey("empires.id"), nullable=True)
    name: Mapped[str]
    symbol: Mapped[str]
    is_baseline: Mapped[bool] = mapped_column(default=False)
    exchange_rate: Mapped[float] = mapped_column(default=1.0)

    empire: Mapped[Optional["Empire"]] = relationship(back_populates="currencies")

    def __init__(self, name:str, symbol:str, empire_id: Optional[int] = None, is_baseline: bool = False, exchange_rate: float = 1.0):
        self.name = name
        self.symbol = symbol
        self.empire_id = empire_id
        self.is_baseline = is_baseline
        self.exchange_rate = exchange_rate

    