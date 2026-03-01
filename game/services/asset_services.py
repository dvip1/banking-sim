from sqlalchemy.orm import Session
from game.models.empire import Empire
from game.models.assets import Asset
from game.models.currency import Currency
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from game.models.empire import Empire
    from game.models.assets import Asset
    from game.models.currency import Currency

class AssetService:
    def __init__(self, session: Session):
        self.session = session
    
    def research_asset(self, asset: Asset, currency: Optional[Currency] = None):
        if asset.is_researched:
            raise ValueError("Asset is already researched")
        if currency is None:
            from game.models.bank import Bank
            currency = Bank._resolve_currency(None, self.session)
        empire = asset.empire
        if empire.bank.get_balance(currency, session=self.session) < asset.base_cost:
            raise ValueError("Insufficient funds to research asset")
        empire.bank.pay_wages(currency, asset.base_cost, session=self.session)
        asset.is_researched = True
        self.session.commit()
        return asset
    
