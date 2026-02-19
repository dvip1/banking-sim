from .models.empire import Empire
class Game:
    def __init__(self, name):
        self.name = name
        self.empire = Empire("khmer")
    def start(self):
        asset1 = self.empire.new_asset("Savings Account", 100)
        asset2 = self.empire.new_asset("Checking Account", 150)
        print(asset1.research_status())
        print(asset2.research_status())

    