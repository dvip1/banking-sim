from sqlalchemy.orm import Mapped, mapped_column, relationship, Session
from sqlalchemy import ForeignKey
from typing import List, TYPE_CHECKING, Optional

from ..database import Base
from ..services.currency_service import CurrencyService

if TYPE_CHECKING:
    from .game import Game
    from .assets import Asset
    from .currency import Currency
    from .balance import EmpireBalance
    from .bank import Bank
    from ..services.currency_service import CurrencyService

class Empire(Base): 
    __tablename__ = "empires"

    id: Mapped[int] = mapped_column(primary_key=True)
    game_id: Mapped[int] = mapped_column(ForeignKey("games.id"))
    name: Mapped[str]
    population: Mapped[int] = mapped_column(default=1)
    # Gold is now a global currency, no longer a column here
    happiness: Mapped[float] = mapped_column(default=1.0)
    
    # Relationships
    game: Mapped["Game"] = relationship(back_populates="empires")
    assets: Mapped[List["Asset"]] = relationship(back_populates="empire", cascade="all, delete-orphan")
    currencies: Mapped[List["Currency"]] = relationship(back_populates="empire")
    balances: Mapped[List["EmpireBalance"]] = relationship(back_populates="empire", cascade="all, delete-orphan")
    bank: Mapped["Bank"] = relationship(back_populates="empire", uselist=False, cascade="all, delete-orphan")

    def __init__(self, name: str, game_id: int, session: Optional[Session] = None):
        self.name = name
        self.game_id = game_id
        self.add_bank_if_not_exists(session)
        self.happiness = 1.0
        self.population = 1

        
    @property
    def researched_assets(self) -> List["Asset"]:
        return [a for a in self.assets if a.is_researched]

    @property
    def not_researched_assets(self) -> List["Asset"]:
         return [a for a in self.assets if not a.is_researched]

    def __repr__(self):
        return f"<Empire: {self.name} | Population: {self.population} | Happiness: {self.happiness:.2f} | Assets: {len(self.assets)}>"

    def new_asset(self, name:str, base_cost:float):
        from .assets import Asset
        asset = Asset(name=name, base_cost=base_cost, empire_id=self.id)
        self.assets.append(asset)
        return asset
    
    def modify_workers(self, change:int):
        self.population += change # Assuming worker_available maps to population or logic needs update
        # original code had worker_available separate from population?
        # "self.worker_available = self.population" in init
        # keeping it simple for now, using population as workers
        self.population = max(0, self.population)
        return self.population   
    
    def add_bank_if_not_exists(self, session: Optional[Session] = None):
        from .bank import Bank
        if not self.bank:
            self.bank = Bank(empire_id=self.id, session=session)
        elif session is not None:
            self.bank._session = session
        return self.bank

    @property
    def total_wealth(self) -> float:
        """
        Calculates the total wealth of the empire converted to the baseline currency.
        Assumes that the baseline currency has exchange_rate = 1.0 (or logic handles conversion relative to it).
        Row-level calculation: balance.amount * balance.currency.exchange_rate
        """
        return sum(b.amount * b.currency.exchange_rate for b in self.balances)    