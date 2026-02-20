import uuid
import math
import random
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from typing import TYPE_CHECKING

from ..database import Base

if TYPE_CHECKING:
    from .empire import Empire

class Asset(Base):
    __tablename__ = "assets"

    id: Mapped[int] = mapped_column(primary_key=True)
    empire_id: Mapped[int] = mapped_column(ForeignKey("empires.id"))
    name: Mapped[str]
    base_cost: Mapped[float]
    
    # We can keep uuid as a separate column if needed, or relying on int ID.
    # The original code had self.id = str(uuid.uuid4())[:8]
    # Let's keep a public_id for that.
    public_id: Mapped[str] = mapped_column(default=lambda: str(uuid.uuid4())[:8])

    # 2. Research State (The "Development")
    is_researched: Mapped[bool] = mapped_column(default=False)
    research_progress: Mapped[float] = mapped_column(default=0.0)
    research_turn_taken: Mapped[int] = mapped_column(default=1)
    research_total_turn: Mapped[int] = mapped_column(default=1) # check if this is static or derived?
    
    # 3. Production State (The "Factory")
    units_produced: Mapped[int] = mapped_column(default=0)
    inventory: Mapped[int] = mapped_column(default=0)
    
    # Properties that are not columns but computed/random could be fields or ignore?
    # predict_value was random in init. We should probably store it if we want persistence.
    predict_value: Mapped[float] = mapped_column(default=0.0)
    
    empire: Mapped["Empire"] = relationship(back_populates="assets")

    def __init__(self, name:str, base_cost:float, empire_id: int):
        self.name = name
        self.base_cost = base_cost
        self.empire_id = empire_id
        self.predict_value = self._gaussian_float(base_cost*0.6, base_cost*1.5)
        # Defaults handled by mapped_column or here
        self.is_researched = False
        self.research_progress = 0.0

    def __repr__(self):
        status = "Researched" if self.is_researched else f"Researching ({self.research_progress:.1%})"
        return f"<Asset: {self.name} | Cost: {self.base_cost} | {status}>"

    # --- Core Logic Stubs ---


    @property
    def is_research(self):
        return self.is_researched

    def research_status(self):
        """
        Empire calls this to check research status and decide whether to invest in research this turn. 
        """
        dic = {
            "is_researched": self.is_researched,
            "research_progress": self.research_progress,
            "predict_value": self.predict_value,
        }
        return dic


    @staticmethod 
    def _gaussian_int(low, high, sigma=0.16):
        """Helper function to generate a random integer with a Gaussian distribution."""
        mean = (low + high) / 2
        value = random.gauss(mean, sigma * (high - low))
        return max(low, min(high, int(round(value))))

    @staticmethod
    def _gaussian_float(low, high, sigma=0.08):
        mean = (low + high) / 2
        std = sigma * (high - low)

        while True:  # resample to avoid boundary spikes
            value = random.gauss(mean, std)
            if low <= value <= high:
                return value

    def info(self):
        """""
        Returns a dict of all the raw data about the asset,
        """
        info = {
            "id": self.id,
            "name": self.name,
            "base_cost": self.base_cost,
            "is_researched": self.is_researched,
            "research_progress": self.research_progress,
            "units_produced": self.units_produced,
            "inventory": self.inventory
        }
        return info

    def invest_in_research(self, amount, workers):
        """
        Empire calls this to advance research.
        TODO: Implement formula for how much progress 'gold + workers' buys.
        TODO: Check if progress >= 1.0, then set self.is_researched = True.
        """
        if self.is_researched:
            return "Already Researched"
        
        # Placeholder
        pass

    def produce(self, quantity, gold_available, workers):
        """
        Empire calls this to build units.
        TODO: Calculate cost for this specific batch (incorporating efficiency).
        TODO: Check if empire has enough gold.
        TODO: Update self.units_produced and self.inventory.
        """
        if not self.is_researched:
            return "Must research first!"

        # Placeholder
        print(f"Attempting to produce {quantity} units...")
        pass

    def get_production_estimate(self, quantity):
        """
        Forecasting tool.
        Returns: (total_cost, cost_per_unit)
        
        TODO: Implement the 'Learning Curve' math here.
        TODO: Calculate how much cheaper unit #100 is vs unit #1.
        """
        # Placeholder: Return base cost for now
        total = quantity * self.base_cost
        return total, self.base_cost