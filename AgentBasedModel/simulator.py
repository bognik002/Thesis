import random

from AgentBasedModel.agents import ExchangeAgent, Universalist

from AgentBasedModel.utils.math import *
from tqdm import tqdm


class Simulator:
    """
    Simulator is responsible for launching agents' actions and executing scenarios
    """
    def __init__(self, exchange: ExchangeAgent = None, traders: list = None):
        random.shuffle(traders)

        self.exchange = exchange
        self.traders = traders
        self.info = SimulatorInfo(self.exchange, self.traders)  # links to existing objects

    def _payments(self):
        for trader in self.traders:
            # Dividend payments
            trader.cash += trader.assets * self.exchange.dividend()  # allow negative dividends
            # Interest payment
            trader.cash += trader.cash * self.exchange.risk_free  # allow risk-free loan

    def simulate(self, n_iter) -> object:
        for it in tqdm(range(n_iter), desc='Simulation'):
            # Capture current info
            self.info.capture()

            # Call Traders
            for trader in self.traders:
                trader.call()

            # Payments and dividends
            self._payments()  # pay dividends
            self.exchange.call()  # generate next dividends

            # Change behaviour
            if not it % 5 and it > 0:
                returns_std = std([mean(self.info.returns(trader, last=5)) for trader in self.traders])
                for trader in self.traders:
                    if type(trader) == Universalist:
                        ab_returns = self.info.abnormal_returns(trader, last=5)
                        if mean(ab_returns) / returns_std < random.normalvariate(0, 1):
                            trader.change()

        return self


class SimulatorInfo:
    """
    SimulatorInfo is responsible for capturing data during simulating
    """

    def __init__(self, exchange: ExchangeAgent = None, traders: list = None):
        self.exchange = exchange
        self.traders = {t.id: {'name': t.name, 'link': t} for t in traders}

        # Market Statistics
        self.prices = list()  # price at the end of iteration
        self.spreads = list()  # bid-ask spreads
        self.dividends = list()  # dividend paid at each iteration
        self.orders = list()  # order book statistics

        # Agent statistics
        self.equities = list()  # agent: equity
        self.cash = list()  # agent: cash
        self.assets = list()  # agent: number of assets
        self.types = list()  # agent: current type

        """
        # Market Statistics
        self.prices = list()  # price at the end of iteration
        self.spreads = list()  # bid-ask spreads
        self.spread_sizes = list()  # bid-ask spread sizes
        self.dividends = list()
        self.orders_quantities = list()  # list -> (bid, ask)
        self.orders_volumes = list()  # list -> (bid, ask) -> (sum, mean, q1, q3, std)
        self.orders_prices = list()  # list -> (bid, ask) -> (mean, q1, q3, std)

        # Agent Statistics
        self.equity = list()  # sum of equity of agents
        self.cash = list()  # sum of cash of agents
        self.assets_qty = list()  # sum of number of assets of agents
        self.assets_value = list()  # sum of value of assets of agents
        """

    # todo как быть с разными аттрибутами разных типов агентов
    # todo как быть с разными типами агентов, они динамические
    # todo может рандомно инициализировать access, step, etc. в начале у Universalist, записывать их сразу?
    def capture(self):
        """
        Method called at the end of each iteration to capture basic info on simulation.

        **Attributes:**

        *Market Statistics*

        - :class:`list[float]` **prices** --> stock prices on each iteration
        - :class:`list[dict]` **spreads** --> order book spreads on each iteration
        - :class:`list[float]` **dividends** --> dividend paid on each iteration
        - :class:`list[dict[dict]]` **orders** --> order book price, volume, quantity stats on each iteration

        *Traders Statistics*

        - :class:`list[dict]` **equities** --> each agent's equity on each iteration
        - :class:`list[dict]` **cash** --> each agent's cash on each iteration
        - :class:`list[dict]` **assets** --> each agent's number of stocks on each iteration
        - :class:`list[dict]` **types** --> each agent's type on each iteration
        """
        # Market Statistics
        self.prices.append(self.exchange.price())
        self.spreads.append((self.exchange.spread()))
        self.dividends.append(self.exchange.dividend())
        self.orders.append({
            'quantity': {'bid': len(self.exchange.order_book['bid']), 'ask': len(self.exchange.order_book['ask'])},
            # 'price mean': {
            #     'bid': mean([order.price for order in self.exchange.order_book['bid']]),
            #     'ask': mean([order.price for order in self.exchange.order_book['ask']])},
            # 'price std': {
            #     'bid': std([order.price for order in self.exchange.order_book['bid']]),
            #     'ask': std([order.price for order in self.exchange.order_book['ask']])},
            # 'volume sum': {
            #     'bid': sum([order.qty for order in self.exchange.order_book['bid']]),
            #     'ask': sum([order.qty for order in self.exchange.order_book['ask']])},
            # 'volume mean': {
            #     'bid': mean([order.qty for order in self.exchange.order_book['bid']]),
            #     'ask': mean([order.qty for order in self.exchange.order_book['ask']])},
            # 'volume std': {
            #     'bid': std([order.qty for order in self.exchange.order_book['bid']]),
            #     'ask': std([order.qty for order in self.exchange.order_book['ask']])}
        })

        # Trader Statistics
        self.equities.append({t_id: t['link'].equity() for t_id, t in self.traders.items()})
        self.cash.append({t_id: t['link'].cash for t_id, t in self.traders.items()})
        self.assets.append({t_id: t['link'].assets for t_id, t in self.traders.items()})
        self.types.append({t_id: t['link'].type for t_id, t in self.traders.items()})

    # Advanced Statistics
    def returns(self, trader=None, rolling: int = 1, last: int = None) -> list:
        if last is None:  # if not need to return last n, determine starting index
            last = len(self.equities) - 1

        if trader is None:
            eq = [mean(v.values()) for v in self.equities[-last + 1:]]
        else:
            eq = [v[trader.id] for v in self.equities[-last + 1:]]

        r = [(eq[i] - eq[i-1]) / eq[i-1] for i in range(len(eq)) if i > 0]  # calculate returns
        r_rolled = [mean(r[i-rolling:i]) for i in range(len(r) + 1) if i - rolling >= 0]  # apply rolling

        return r_rolled

    def abnormal_returns(self, trader, rolling: int = 1, last: int = None) -> list:
        tr_returns = self.returns(trader, rolling, last)
        all_returns = self.returns(None, rolling, last)
        return [tr_returns[i] - all_returns[i] for i in range(len(all_returns))]
