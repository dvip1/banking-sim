from sqlalchemy.orm import Mapped, mapped_column, relationship, Session
from typing import List, Optional
from ..database import Base, SessionLocal, engine
from .empire import Empire

class Game(Base):
    __tablename__ = "games"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)
    turn: Mapped[int] = mapped_column(default=0)

    empires: Mapped[List["Empire"]] = relationship(back_populates="game", cascade="all, delete-orphan")
    
    def __init__(self, name: str):
        self.name = name
        self.turn = 0

    def __repr__(self):
        return f"<Game(id={self.id}, name={self.name}), turn={self.turn})>"
    
    @property
    def turn_number(self) -> int:
        return self.turn
    def next_turn(self):
        self.turn += 1
        return self.turn
    
    def add_empire(self, empire:Empire):
        if empire not in self.empires:
            self.empires.append(empire)
        return empire

    def distribute_global_currency(self, empire: Empire, session: Optional[Session] = None):
        turn = self.turn
        amount = 5.0000  # Amount of global currency to distribute each turn
        if turn <100:
            empire.bank.deposit(None, amount, session=session)  # Deposit baseline currency
        else:
            print(f"Turn {turn}: No more global currency distribution.")
