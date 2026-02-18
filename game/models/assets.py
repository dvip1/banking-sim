import uuid
import math
import random

class Asset:
    def __init__(self, name:str, base_cost:float, base_value:float):
        # 1. Identity & Base Stats (The "Concept")
        self.id = str(uuid.uuid4())[:8]  # Unique ID for sharing
        self.name = name
        self.base_cost = base_cost       # Base Gold to produce ONE unit (before efficiency)
        self.base_value = base_value     # Happiness/Power value
        
        # 2. Research State (The "Development")
        self.is_researched = False
        self.research_progress = 0.0     # 0.0 to 1.0 (100%)
        self.research_cost_total = base_cost * 10  # Arbitrary multiplier for now
        
        # 3. Production State (The "Factory")
        self.units_produced = 0          # Total history count (affects learning curve)
        self.inventory = 0               # Current stock available to use

    def __repr__(self):
        status = "Researched" if self.is_researched else f"Researching ({self.research_progress:.1%})"
        return f"<Asset: {self.name} | Cost: {self.base_cost} | {status}>"

    # --- Core Logic Stubs ---

    def invest_in_research(self, gold_amount, workers):
        """
        Empire calls this to advance research.
        TODO: Implement formula for how much progress 'gold + workers' buys.
        TODO: Check if progress >= 1.0, then set self.is_researched = True.
        """
        if self.is_researched:
            return "Already Researched"
        
        # Placeholder
        print(f"Investing {gold_amount} Gold and {workers} Workers...")
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