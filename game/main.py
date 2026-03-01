from sqlalchemy import select

from .models.empire import Empire
from .models.game import Game as GameModel
from .services.empire_services import EmpireService

class Main:
    def __init__(self, name, session):
        self.name = name
        self.session = session
        created = False

        self.model = self.session.execute(
            select(GameModel).where(GameModel.name == name)
        ).scalar_one_or_none()
        if self.model is None:
            self.model = GameModel(name=name)
            self.session.add(self.model)
            self.session.flush()  # gets self.model.id
            created = True

        self.empire = self.session.execute(
            select(Empire).where(
                Empire.name == "khmer",
                Empire.game_id == self.model.id,
            )
        ).scalar_one_or_none()
        if self.empire is None:
            self.empire = Empire("khmer", self.model.id, session=self.session)
            self.model.add_empire(self.empire)
            self.session.add(self.empire)
            created = True
        else:
            self.empire.add_bank_if_not_exists(self.session)

        if created:
            self.session.commit()
    

    def start(self):
        next_turn = 'n'
        end_game = 'e'
        while next_turn != end_game:
            print(f"Turn {self.model.turn_number}:")
            print(f"Empire: {self.empire.name}, Balance: {self.empire.bank.get_balance(None, session=self.session)} Gold")
            next_turn = input("Press 'n' for next turn, 'a' to create assets,'e' to end game: ").lower()
            if next_turn == 'n':
                self.model.next_turn()
                self.model.distribute_global_currency(self.empire, session=self.session)
                self.session.commit()
            elif next_turn == 'e':
                print("Ending game. Thanks for playing!")
            elif next_turn == 'a':
                asset_name = input("Enter asset name: ")
                base_cost = float(input("Enter asset base cost: "))
                emp_service = EmpireService(self.session)
                try:
                    emp_service.new_asset(self.empire, asset_name, base_cost, None, None)  
                except ValueError as e:
                    print(f"Error creating asset: {e}")
                self.session.commit()
                print(f"Asset '{asset_name}' created with base cost {base_cost}.")
            else:
                print("Invalid input, please try again.")