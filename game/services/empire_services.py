from sqlalchemy.orm import Session
from typing import TYPE_CHECKING

from game.data.assets_data import AssetCategory
from ..models.empire import Empire
from game.models.assets import Asset

if TYPE_CHECKING:
    from ..models.empire import Empire
    from game.models.assets import Asset

class EmpireService:
    def __init__(self,session:Session):
        self.session = session
    
    def _new_asset(self, empire:Empire,name:str, base_cost:float, category:AssetCategory):
        asset = Asset(name=name, base_cost=base_cost, empire_id=empire.id, category=category)
        self.session.add(asset)
        self.session.commit()
        return asset
    
    def new_asset_healthcare(self, empire:Empire, name:str, base_cost:float):
        return self._new_asset(empire, name, base_cost, AssetCategory.HEALTHCARE)
    
    def new_asset_maintain_population(self, empire:Empire, name:str, base_cost:float):
        return self._new_asset(empire, name, base_cost, AssetCategory.SUSTENANCE)

    def new_asset_luxury(self, empire:Empire, name:str, base_cost:float):
        return self._new_asset(empire, name, base_cost, AssetCategory.LUXURY)

    def new_asset_contraband(self, empire:Empire, name:str, base_cost:float):
        return self._new_asset(empire, name, base_cost, AssetCategory.CONTRABAND)