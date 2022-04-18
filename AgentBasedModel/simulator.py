from AgentBasedModel.agents import ExchangeAgent

from AgentBasedModel.utils.math import *
from tqdm import tqdm


class Simulator:
    """
    Simulator is responsible for launching agents' actions and executing scenarios
    """
    def __init__(self, exchange: ExchangeAgent = None, traders: list = None):
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

            # Call exchange (dividends)
            self._payments()
            self.exchange.call()

        return self


class SimulatorInfo:
    """
    SimulatorInfo is responsible for capturing data during simulating
    """

    # todo добавить статистики для агентов
    def __init__(self, exchange: ExchangeAgent = None, traders: list = None):
        self.exchange = exchange
        self.traders = traders

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

    # todo добавить вычисления статистик для агентов
    def capture(self):
        """
        Method called at the end of each iteration to capture current statistics on market
        """
        # Market Statistics
        self.prices.append(self.exchange.price())
        self.spreads.append((self.exchange.spread()))
        self.dividends.append(self.exchange.dividend())
        self.orders_quantities.append({
            'bid': len(self.exchange.order_book['bid']),
            'ask': len(self.exchange.order_book['ask'])
        })
        tmp_bid = [order.qty for order in self.exchange.order_book['bid']]
        tmp_ask = [order.qty for order in self.exchange.order_book['ask']]
        self.orders_volumes.append({
            'bid': {
                'sum': sum(tmp_bid),
                'mean': mean(tmp_bid),
                'q1': quantile(tmp_bid, .25),
                'q3': quantile(tmp_bid, .75),
                'std': std(tmp_bid)
            },
            'ask': {
                'sum': sum(tmp_ask),
                'mean': mean(tmp_ask),
                'q1': quantile(tmp_ask, .25),
                'q3': quantile(tmp_ask, .75),
                'std': std(tmp_ask)
            }
        })
        tmp_bid = [order.price for order in self.exchange.order_book['bid']]
        tmp_ask = [order.price for order in self.exchange.order_book['ask']]
        self.orders_prices.append({
            'bid': {
                'mean': mean(tmp_bid),
                'q1': quantile(tmp_bid, .25),
                'q3': quantile(tmp_bid, .75),
                'std': std(tmp_bid)
            },
            'ask': {
                'mean': mean(tmp_ask),
                'q1': quantile(tmp_ask, .25),
                'q3': quantile(tmp_ask, .75),
                'std': std(tmp_ask)
            }
        })
        self.spread_sizes.append(self.exchange.spread()['ask'] - self.exchange.spread()['bid'])

        # Agent Statistics
        self.equity.append(sum([trader.equity() for trader in self.traders]))
        self.cash.append(sum([trader.cash for trader in self.traders]))
        self.assets_qty.append(sum([trader.assets for trader in self.traders]))
        self.assets_value.append(self.equity[-1] - self.cash[-1])
