from agents.main import Agent

class StandardAgent(Agent):
    def __init__(self,name, session, game_id):
        super().__init__(name, session, game_id)
    def make_decision(self):
        # Implement a simple decision-making process for the standard agent
        # For example, the agent could prioritize research, then production, then trading
        if self.empire.not_researched_assets:
            self.researcher()
        elif self.empire.population < 10:  # Arbitrary threshold for population growth
            self.producer()
        else:
            self.trader()
    def researcher(self):
        print(f"{self.name} is researching new assets.")