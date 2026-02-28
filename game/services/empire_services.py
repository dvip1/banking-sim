from sqlalchemy.orm import Session
from typing import TYPE_CHECKING

from game.data.assets_data import AssetCategory
from ..models.empire import Empire
from game.models.assets import Asset
from game.models.currency import Currency
from game.models.bank import Bank

if TYPE_CHECKING:
    from ..models.empire import Empire
    from game.models.assets import Asset
    from game.models.currency import Currency
    from game.models.bank import Bank 

class EmpireService:
    def __init__(self,session:Session):
        self.session = session
    
    def _new_asset(self, empire:Empire,name:str, base_cost:float, category:AssetCategory):
        asset = Asset(name=name, base_cost=base_cost, empire_id=empire.id, category=category)
        self.session.add(asset)
        self.session.commit()
        return asset
    
    def new_asset(self, empire:Empire, name:str, base_cost:float, currency: Currency, category: AssetCategory):
        """
        Docstring for new_asset
        
        :param self: Description
        :param empire: Description
        :type empire: Empire
        :param name: Description
        :type name: str
        :param base_cost: Description
        :type base_cost: float
        :param currency: Description
        :type currency: Currency
        :param category: Description
        :type category: AssetCategory
        """

        if currency is None:
            raise ValueError("Currency must be provided for assets")
        bank = empire.bank
        if bank.get_balance(currency, session=self.session) < base_cost:
            raise ValueError("Insufficient funds to create asset")
        bank.pay_wages(currency, base_cost, session=self.session)
        return self._new_asset(empire, name, base_cost, category)

    def discovered_assets(self, empire:Empire):
        #not researched assets are those that have been created but not yet fully researched
        return [a for a in empire.assets if not a.is_researched]

    def researched_assets(self, empire:Empire):
        #researched assets are those that have been fully researched and are providing benefits to the empire
        return [a for a in empire.assets if a.is_researched]

     