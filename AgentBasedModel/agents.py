from AgentBasedModel.exchange import ExchangeAgent
from AgentBasedModel.utils import Order
import random


class Trader:
    def __init__(self, market: ExchangeAgent, cash: float or int, assets: int = 0):
        self.name = 'Undefined'

        self.market = market
        self.orders = list()

        self.cash = cash
        self.assets = assets

    def __str__(self) -> str:
        return self.name

    def equity(self):
        price = self.market.price() if self.market.price() is not None else 0
        return self.cash + self.assets * price

    def _buy_limit(self, quantity, price):
        order = Order(price, quantity, 'bid', self)
        self.orders.append(order)
        self.market.limit_order(order)

    def _sell_limit(self, quantity, price):
        order = Order(price, quantity, 'ask', self)
        self.orders.append(order)
        self.market.limit_order(order)

    def _buy_market(self, quantity) -> int:
        """
        :return: quantity unfulfilled
        """
        if not self.market.order_book['ask']:
            return quantity
        order = Order(self.market.order_book['ask'].last.price, quantity, 'bid', self)
        return self.market.market_order(order).qty

    def _sell_market(self, quantity) -> int:
        """
        :return: quantity unfulfilled
        """
        if not self.market.order_book['bid']:
            return quantity
        order = Order(self.market.order_book['bid'].last.price, quantity, 'ask', self)
        return self.market.market_order(order).qty

    def _cancel_order(self, order: Order):
        self.market.cancel_order(order)
        self.orders.remove(order)


class NoiseTrader(Trader):
    """
    NoiseTrader perform action on call. Creates noisy orders to recreate trading in real environment.
    """
    id = 0

    def __init__(self, market: ExchangeAgent, cash: float or int, assets: int = 0):
        super().__init__(market, cash, assets)
        self.name = f'NoiseTrader{self.id}'
        NoiseTrader.id += 1

    def _draw_price(self, order_type, spread: dict, lamb=1) -> float:
        """
        Draw price for limit order of Noise Agent. The price is calculated as:
        1) 35% - within the spread - uniform distribution
        2) 65% - out of the spread - delta from best price is exponential distribution r.v.

        :return: price
        """
        random_state = random.random()  # Determines IN spread OR OUT of spread

        # Within the spread
        if random_state < .35:
            return random.uniform(spread['bid'], spread['ask'])

        # Out of spread
        else:
            delta = random.expovariate(lamb)
            if order_type == 'bid':
                return round(spread['bid'] - delta, 2)
            if order_type == 'ask':
                return round(spread['ask'] + delta, 2)

    def _draw_quantity(self, order_exec, a=1, b=10) -> float:
        """
        Draw quantity for any order of Noise Agent.
        1) If market order - currently the same as for limit order
        2) If limit order - volume is derived from log-normal distribution

        :param order_exec: 'market' or 'limit'
        :return: quantity for order
        """
        # Market order
        if order_exec == 'market':
            return random.randint(a, b)

        # Limit order
        if order_exec == 'limit':
            return random.randint(a, b)

    def call(self):
        """
        Function to call agent action

        :param spread: {'bid': float, 'ask' float} - spread stamp with lag
        :return: void
        """
        spread = self.market.spread()
        if spread is None:
            return

        random_state = random.random()

        if random_state > .5:
            order_type = 'bid'
        else:
            order_type = 'ask'

        random_state = random.random()
        # Market order
        if random_state > .85:
            quantity = self._draw_quantity('market')
            if order_type == 'bid':
                self._buy_market(quantity)
            elif order_type == 'ask':
                self._sell_market(quantity)

        # Limit order
        elif random_state > .5:
            price = self._draw_price(order_type, spread)
            quantity = self._draw_quantity('limit')
            if order_type == 'bid':
                self._buy_limit(quantity, price)
            elif order_type == 'ask':
                self._sell_limit(quantity, price)

        # Cancellation order
        elif random_state < .5:
            if self.orders:
                order_n = random.randint(0, len(self.orders) - 1)
                self._cancel_order(self.orders[order_n])
