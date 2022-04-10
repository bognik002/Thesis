from AgentBasedModel.exchange import ExchangeAgent
from AgentBasedModel.agents import NoiseTrader

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

    def simulate(self, n_iter) -> object:
        for it in tqdm(range(n_iter), desc='Simulation'):
            # Capture current info
            self.info.capture()

            # Call Traders
            for trader in self.traders:
                trader.call()

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
        self.orders_quantities = list()  # list -> (bid, ask)
        self.orders_volumes = list()  # list -> (bid, ask) -> (sum, mean, q1, q3, std)
        self.orders_prices = list()  # list -> (bid, ask) -> (mean, q1, q3, std)
        self.spread_sizes = list()  # bid-ask spread
        self.equity = list()  # sum of equity of agents

        # Agent Statistics
        # ...

    # todo добавить вычисления статистик для агентов
    def capture(self):
        """
        Method called at the end of each iteration to capture current statistics on market
        """
        # Market Statistics
        self.prices.append(self.exchange.price())
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
        self.equity.append(sum([trader.equity() for trader in self.traders]))

        # Agent Statistics
        # ...
