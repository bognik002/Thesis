from AgentBasedModel.agents import ExchangeAgent

from AgentBasedModel.utils.math import *
from tqdm import tqdm


class Simulator:
    """
    Simulator is responsible for launching agents' actions and executing scenarios
    """
    def __init__(self, exchange: ExchangeAgent = None, traders: list = None):
        self.exchange = exchange
        self.traders = traders  # todo Сделать рандомный порядок для агентов (shuffle)
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

            self._payments()  # pay dividends
            self.exchange.call()  # generate next dividends

        return self


class SimulatorInfo:
    """
    SimulatorInfo is responsible for capturing data during simulating
    """

    def __init__(self, exchange: ExchangeAgent = None, traders: list = None):
        self.exchange = exchange
        self.traders = {t.id: {'name': t.name, 'link': t, 'order': i} for i, t in enumerate(traders)}

        # Market Statistics
        self.prices = list()  # price at the end of iteration
        self.spreads = list()  # bid-ask spreads
        self.dividends = list()  # dividend paid at each iteration
        self.orders = list()  # order book statistics

        # Agent statistics
        self.equities = list()  # agent: equity
        self.cash = list()  # agent: cash
        self.assets = list()  # agent: number of assets

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
        Method called at the end of each iteration to capture current statistics on market
        """
        # Market Statistics
        self.prices.append(self.exchange.price())
        self.spreads.append((self.exchange.spread()))
        self.dividends.append(self.exchange.dividend())
        self.orders.append({
            'quantity': {'bid': len(self.exchange.order_book['bid']), 'ask': len(self.exchange.order_book['ask'])},
            'price mean': {
                'bid': mean([order.price for order in self.exchange.order_book['bid']]),
                'ask': mean([order.price for order in self.exchange.order_book['ask']])},
            'price std': {
                'bid': std([order.price for order in self.exchange.order_book['bid']]),
                'ask': std([order.price for order in self.exchange.order_book['ask']])},
            'volume sum': {
                'bid': sum([order.qty for order in self.exchange.order_book['bid']]),
                'ask': sum([order.qty for order in self.exchange.order_book['ask']])},
            'volume mean': {
                'bid': mean([order.qty for order in self.exchange.order_book['bid']]),
                'ask': mean([order.qty for order in self.exchange.order_book['ask']])},
            'volume std': {
                'bid': std([order.qty for order in self.exchange.order_book['bid']]),
                'ask': std([order.qty for order in self.exchange.order_book['ask']])}
        })

        # Trader Statistics
        self.equities.append({t_id: t.equity() for t_id, t in self.traders.items()})
        self.cash.append({t_id: t.cash for t_id, t in self.traders.items()})
        self.assets.append({t_id: t.assets for t_id, t in self.traders.items()})


        """self.equity.append(sum([trader.equity() for trader in self.traders]))
        self.cash.append(sum([trader.cash for trader in self.traders]))
        self.assets_qty.append(sum([trader.assets for trader in self.traders]))
        self.assets_value.append(self.equity[-1] - self.cash[-1])"""
