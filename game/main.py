from sqlalchemy import select

from .models.empire import Empire
from .models.game import Game as GameModel
from .database import SessionLocal, Base, engine

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
            next_turn = input("Press 'n' for next turn, 'e' to end game: ").lower()
            if next_turn == 'n':
                self.model.next_turn()
                self.empire.bank.deposit(None, 5.0000, session=self.session)  # Deposit 5 gold each turn
                self.session.commit()  
            elif next_turn == 'e':
                print("Ending game. Thanks for playing!")
            else:
                print("Invalid input, please try again.")


    