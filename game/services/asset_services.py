from sqlalchemy.orm import Session
from game.models.empire import Empire
from typing import Optional

class AssetService:
    def __init__(self, session: Session):
        self.session = session

