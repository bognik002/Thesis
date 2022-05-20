from AgentBasedModel.simulator import Simulator
from AgentBasedModel.agents import Universalist, Fundamentalist, MarketMaker


class Event:
    def __init__(self, it: int):
        self.it = it  # Activation it
        self.simulator = None

    def call(self, it: int):
        if self.simulator is None:
            raise Exception('No simulator link found')
        if it != self.it:
            return True

    def link(self, simulator: Simulator):
        self.simulator = simulator
        return self


class PriceShock(Event):
    def __init__(self, it: int, price_change: float):
        super().__init__(it)
        self.dp = price_change

    def call(self, it: int):
        if super().call(it):
            return
        divs = self.simulator.exchange.dividend_book  # link to dividend book
        r = self.simulator.exchange.risk_free  # risk-free rate

        self.simulator.exchange.dividend_book = [div + self.dp * r for div in divs]


class InformationShock(Event):
    def __init__(self, it, access: int):
        super().__init__(it)
        self.access = access

    def call(self, it: int):
        if super().call(it):
            return
        for trader in self.simulator.traders:
            if type(trader) in (Universalist, Fundamentalist):
                trader.access = self.access


class MarketMakerIn(Event):
    def __init__(self, it, cash: float = 5e4):
        super().__init__(it)
        self.cash = cash

    def call(self, it: int):
        if super().call(it):
            return

        maker = MarketMaker(self.simulator.exchange, self.cash)
        self.simulator.traders.append(maker)


class MarketMakerOut(Event):
    def __init__(self, it):
        super().__init__(it)

    def call(self, it: int):
        if super().call(it):
            return

        self.simulator.traders = [tr for tr in self.simulator.traders if type(tr) != MarketMaker]


class TransactionCost(Event):
    def __init__(self, it, cost):
        super().__init__(it)
        self.cost = cost

    def call(self, it: int):
        if super().call(it):
            return

        self.simulator.exchange.transaction_cost = self.cost
