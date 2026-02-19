from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List, Optional
from ..database import Base

class Game(Base):
    __tablename__ = "games"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)

    empires: Mapped[List["Empire"]] = relationship(back_populates="game", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Game(id={self.id}, name={self.name})>"
