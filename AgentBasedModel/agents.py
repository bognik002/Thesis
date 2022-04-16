from AgentBasedModel.utils import Order, OrderList
import random


class ExchangeAgent:
    """
    ExchangeAgent implements automatic orders handling within the order book. It supports limit orders,
    market orders, cancel orders, returns current spread prices and volumes.
    """
    id = 0

    def __init__(self, price: float or int = 500, std: float or int = 10, volume: int = 1000, rf: float = 5e-4):
        """
        Initialization parameters
        :param price: stock initial price
        :param std: standard deviation of order prices in book
        :param volume: number of orders in book
        :param rf: risk-free rate (interest rate for cash holdings of agents)
        """
        self.name = f'ExchangeAgent{self.id}'
        ExchangeAgent.id += 1

        self.order_book = {'bid': OrderList('bid'), 'ask': OrderList('ask')}
        self.dividend_book = list()  # list of future dividends
        self.risk_free = rf
        self._fill_book(price, std, volume)

    def call(self):
        """
        Generate time series on future dividends.
        """
        # Generate future dividend
        d = self.dividend_book[-1] + self._next_dividend()
        self.dividend_book.append(max(d, 0))  # dividend > 0
        self.dividend_book.pop(0)

    def _fill_book(self, price, std, volume, div: float = 0.25):
        """
        Fill order book with random orders. Fill dividend book with n future dividends.
        """
        # Order book
        prices1 = [round(random.normalvariate(price - 2*std, std), 1) for _ in range(volume // 2)]
        prices2 = [round(random.normalvariate(price + 2*std, std), 1) for _ in range(volume // 2)]
        quantities = [random.randint(1, 10) for _ in range(volume)]

        for (p, q) in zip(sorted(prices1 + prices2), quantities):
            if p > price:
                order = Order(p, q, 'ask', None)
                self.order_book['ask'].append(order)
            else:
                order = Order(p, q, 'bid', None)
                self.order_book['bid'].push(order)

        # Dividend book
        for i in range(20):
            self.dividend_book.append(max(div, 0))  # dividend > 0
            div += self._next_dividend()

    def _clear_book(self):
        """
        Clears glass from orders with 0 qty.

        complexity O(n)

        :return: void
        """
        self.order_book['bid'] = OrderList.from_list([order for order in self.order_book['bid'] if order.qty > 0])
        self.order_book['ask'] = OrderList.from_list([order for order in self.order_book['ask'] if order.qty > 0])

    def spread(self) -> dict or None:
        """
        :return: {'bid': float, 'ask': float}
        """
        if self.order_book['bid'] and self.order_book['ask']:
            return {'bid': self.order_book['bid'].first.price, 'ask': self.order_book['ask'].first.price}
        return None

    def spread_volume(self) -> dict or None:
        """
        :return: {'bid': float, 'ask': float}
        """
        if self.order_book['bid'] and self.order_book['ask']:
            return {'bid': self.order_book['bid'].first.qty, 'ask': self.order_book['ask'].first.qty}
        return None

    def price(self) -> float or None:
        spread = self.spread()
        if spread:
            return (spread['bid'] + spread['ask']) / 2
        raise Exception(f'Price cannot be determined, since no orders either bid or ask')

    def dividend(self, trader=None) -> list or float:
        """
        Returns current dividend payment value. If called by a trader, returns expectation on future dividends
        given information access.
        """
        if trader is None:
            return self.dividend_book[0]
        return sum(self.dividend_book[:trader.access]) / trader.access

    @classmethod
    def _next_dividend(cls):
        return random.normalvariate(0, 1e-4)

    def limit_order(self, order: Order):
        """
        Executes limit order, fulfilling orders if on other side of spread

        :return: void
        """
        bid, ask = self.spread().values()
        if not bid or not ask:
            return

        if order.order_type == 'bid':
            if order.price >= ask:
                order = self.order_book['ask'].fulfill(order)
            if order.qty > 0:
                self.order_book['bid'].insert(order)
            return

        elif order.order_type == 'ask':
            if order.price <= bid:
                order = self.order_book['bid'].fulfill(order)
            if order.qty > 0:
                self.order_book['ask'].insert(order)

    def market_order(self, order: Order) -> Order:
        """
        Executes market order, fulfilling orders on the other side of spread

        :return: Order
        """
        if order.order_type == 'bid':
            order = self.order_book['ask'].fulfill(order)
        elif order.order_type == 'ask':
            order = self.order_book['bid'].fulfill(order)
        return order

    def cancel_order(self, order: Order):
        """
        Cancel order from order book

        :return: void
        """
        if order.order_type == 'bid':
            self.order_book['bid'].remove(order)
        elif order.order_type == 'ask':
            self.order_book['ask'].remove(order)


class Trader:
    id = 0

    def __init__(self, market: ExchangeAgent, cash: float or int, assets: int = 0, access: int = 1):
        """
        Trader that is activated on call to perform action.

        :param market: link to exchange agent
        :param cash: trader's cash available
        :param assets: trader's number of shares hold
        :param access: number of future dividends informed
        """
        self.name = f'Trader{self.id}'
        self.id += 1

        self.market = market
        self.orders = list()

        self.cash = cash
        self.assets = assets
        self.access = access

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
    def __init__(self, market: ExchangeAgent, cash: float or int, assets: int = 0, access: int = 1):
        super().__init__(market, cash, assets, access)
        self.name = f'Trader{self.id} (NoiseTrader)'

    @staticmethod
    def _draw_price(order_type, spread: dict, std=10) -> float:
        """
        Draw price for limit order of Noise Agent. The price is calculated as:
        1) 35% - within the spread - uniform distribution
        2) 65% - out of the spread - delta from best price is exponential distribution r.v.

        :return: price
        """
        lamb = 1/std
        random_state = random.random()  # Determines IN spread OR OUT of spread

        # Within the spread
        if random_state < .35:
            return random.uniform(spread['bid'], spread['ask'])

        # Out of spread
        else:
            delta = random.expovariate(lamb)
            if order_type == 'bid':
                return round(spread['bid'] - delta, 1)
            if order_type == 'ask':
                return round(spread['ask'] + delta, 1)

    @staticmethod
    def _draw_quantity(order_exec, a=1, b=10) -> float:
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
        elif random_state < .35:
            if self.orders:
                order_n = random.randint(0, len(self.orders) - 1)
                self._cancel_order(self.orders[order_n])


class Fundamentalist(Trader):
    """
    Fundamentalist traders strictly believe in the information they receive. If they find an ask
    order with a price lower or a bid order with a price higher than their estimated present
    value, i.e. E(V|Ij,k), they accept the limit order, otherwise they put a new limit order
    between the former best bid and best ask prices.
    """
    def __init__(self, market: ExchangeAgent, cash: float or int, assets: int = 0, access: int = 1):
        super().__init__(market, cash, assets, access)
        self.name = f'Trader{self.id} (Fundamentalist)'

    def _evaluate(self):
        """
        Evaluate stock using constant dividend model.
        """
        div = self.market.dividend(self)  # expected value of future dividends
        r = self.market.risk_free  # risk-free rate
        return div / r

    def call(self):
        fundamental_price = round(self._evaluate(), 1)
        spread = self.market.spread()

        # Cancel all orders
        if len(self.orders) > 5:
            for order in self.orders:
                self._cancel_order(order)

        random_state = random.random()  # determine order type

        if fundamental_price >= spread['ask']:
            if random_state > .5:
                self._buy_market(random.randint(0, 10))
            else:
                self._sell_limit(random.randint(0, 10), fundamental_price + .1)

        elif fundamental_price <= spread['bid']:
            if random_state > .5:
                self._sell_market(random.randint(0, 10))
            else:
                self._buy_limit(random.randint(0, 10), fundamental_price - .1)

        # Inside the spread
        elif spread['ask'] > fundamental_price > spread['bid']:
            if random_state > .5:
                self._buy_limit(random.randint(0, 10), fundamental_price - .1)
            else:
                self._sell_limit(random.randint(0, 10), fundamental_price + .1)
