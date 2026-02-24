from game.models.empire import Empire
from typing import TYPE_CHECKING 

"""
There are three types of things AI can do:
1. Importer: Can import assets from other empires, possibly at a cost. This is the "import" role.
2. Exporter: Can export assets to other empires, possibly for profit. This is the "export" role.
3. Autarky: Focuses on self-sufficiency, producing everything it needs internally and not engaging in trade. This is the "autarky" role.

These roles can be played in a various ways: 
1. Importer: Focusing on acquiring blueprints, assets to often use it for it's own population 
            and production to export at a margin. This is the "import" role.
2. Exporter: Focusing on producing assets to export to other empires, often for profit. 
            This is the "export" role. 

Now, there are specialization in different techniques. 
1. Trader: Focuses on trading assets with other empires, leveraging market dynamics to maximize profits.
           A trader can become very powerful, but also risky if the market is volatile.
           A market leader Trader can impose it's own currency and exchange rates due to it's market dominance, and can also manipulate the market to its advantage.

2. Researcher: Focuses on researching new assets and technologies, often leading to breakthroughs that can give a competitive edge
               Researcher can specialize in doing research for exporting blueprints to other empires, or could 
               set up a production line to produce the researched assets for export.
               A researcher would ideally need a highly employeed population i.e. good per capita income.
                Population wouldn't matter as much as happiness which is measured by per capital would.

3. Producer: Focuses on producing assets, either for internal use or for export. A producer can optimize production lines,
             manage resources efficiently, and scale up production to meet demand. 
             A Producer would ideally need high population to work in the production lines, and would need to manage the happiness of the population to ensure productivity.


All of them can be a lender or borrower, depending on their financial situation and strategy.

1. Lender: Focuses on lending currency to other empires. 
            They have to be careful with their lending strategy, as it can be profitable but also risky if the borrower defaults.
            Due to the nature of lending, a lender can have a lot of influence over the borrower. 
            Once Lender has it's own currency, it can lend it to spread it's currency and influence other empires, and can also manipulate the exchange rates to its advantage.
            Once a lender has a lot of influence over the borrower, it can also manipulate the borrower's economy to its advantage, and can also use the borrower's resources to further its own goals.

2. Borrower: Focuses on borrowing currency from other empires, often to finance research or production. 
            Borrowers have to be careful with their borrowing strategy, as it can be beneficial but also risky if they take on too much debt or if the lender is not trustworthy.
            A borrower can borrow from multiple leders and invest in their own economy in a cheaper way. 
            But if the borrower is not careful, it can end up in a debt trap, where it has to borrow more and more to pay off existing debt, leading to a downward spiral.
            After defaulting on a loan, the empire has to be careful as the happiness of it's citizens might collapse. Leading to termination of the empire. 


Every Agent would get 5 Global Currency per turn which degrates over time, but other factors like happiness of the empire could contribute
to the amount of currency generated per turn. The agents/empires would stop receiving the global currency entirely after a fixed turn like 100th turn, to encourage them to develop their own economy and currency.
Even after that, agents/empires can trade in global currency and it'd be used as a exchange medium.

After the global currency is phased out, 
the agents/empires can make their own currency or borrow from trusted lenders.
The agents/empires can also trade in global currency and use it as an exchange medium, but it would be more expensive to use global currency as the supply would be limited and demand would be high.
As the trust in other empires/agents shrinks, the demand for global currency would increase, leading to a potential hyperinflation of the global currency.
If the trust grows in other empires/agents, the demand for global currency would decrease, leading to a potential deflation of the global currency.
Currency manipulation and market dynamics would play a crucial role in the economy of the game, and agents would have to navigate these complexities to succeed.

Assets would be the main driver of the economy, and agents would have to research and produce assets to trade with other empires/agents.
Also all of the distinction mentioned here, the agents would use mix of them to best optimize their economy and population. 


"""

if TYPE_CHECKING:
    from game.models.empire import Empire
    from game.models.bank import Bank


class MainAgent:
    def __init__(self, name, session, game_id):
        self.name = name
        self.session = session
        self.empire = Empire(name=self.name, game_id=game_id, session=self.session)

    
    def make_decision(self):
        # Placeholder for decision-making logic
        pass

    def lender(self):
        from game.models.bank import Bank
        # Placeholder for lending logic
        pass

    def borrower(self):
        # Placeholder for borrowing logic
        pass

    def trader(self):
        # Placeholder for trading logic
        pass

    def researcher(self):
        # Placeholder for research logic
        pass

    def producer(self):
        # Placeholder for production logic
        pass