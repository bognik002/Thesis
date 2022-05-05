from AgentBasedModel.utils import Order, OrderList
import random


class ExchangeAgent:
    """
    ExchangeAgent implements automatic orders handling within the order book. It supports limit orders,
    market orders, cancel orders, returns current spread prices and volumes.
    """
    id = 0

    def __init__(self, price: float or int = 100, std: float or int = 5, volume: int = 2000, rf: float = 5e-4):
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

    def _fill_book(self, price, std, volume, div: float = 0.05):
        """
        Fill order book with random orders. Fill dividend book with n future dividends.
        """
        # Order book
        prices1 = [round(random.normalvariate(price - std, std), 1) for _ in range(volume // 2)]
        prices2 = [round(random.normalvariate(price + std, std), 1) for _ in range(volume // 2)]
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

    def dividend(self, access: int = None) -> list or float:
        """
        Returns current dividend payment value. If called by a trader, returns n future dividends
        given information access.
        """
        if access is None:
            return self.dividend_book[0]
        return self.dividend_book[len(self.dividend_book) - access:]

    @classmethod
    def _next_dividend(cls, std=5e-5):
        return random.normalvariate(0, std)

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

    def __init__(self, market: ExchangeAgent, cash: float or int, assets: int = 0):
        """
        Trader that is activated on call to perform action.

        :param market: link to exchange agent
        :param cash: trader's cash available
        :param assets: trader's number of shares hold
        """
        self.type = 'Unknown'
        self.name = f'Trader{self.id}'
        self.id = Trader.id
        Trader.id += 1

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


class Random(Trader):
    """
    Random perform action on call. Creates noisy orders to recreate trading in real environment.
    """
    def __init__(self, market: ExchangeAgent, cash: float or int, assets: int = 0):
        super().__init__(market, cash, assets)
        self.type = 'Random'

    @staticmethod
    def draw_delta(std: float or int = 2.5):
        lamb = 1 / std
        return random.expovariate(lamb)

    @staticmethod
    def draw_price(order_type, spread: dict, std: float or int = 2.5) -> float:
        """
        Draw price for limit order of Noise Agent. The price is calculated as:
        1) 35% - within the spread - uniform distribution
        2) 65% - out of the spread - delta from best price is exponential distribution r.v.
        """
        random_state = random.random()  # Determines IN spread OR OUT of spread

        # Within the spread
        if random_state < .35:
            return random.uniform(spread['bid'], spread['ask'])

        # Out of spread
        else:
            delta = Random.draw_delta(std)
            if order_type == 'bid':
                return round(spread['bid'] - delta, 1)
            if order_type == 'ask':
                return round(spread['ask'] + delta, 1)

    @staticmethod
    def draw_quantity(order_exec, a=1, b=5) -> float:
        """
        Draw random quantity to buy from uniform distribution.

        :param order_exec: 'market' or 'limit'
        :param a: minimal quantity
        :param b: maximal quantity
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
            quantity = self.draw_quantity('market')
            if order_type == 'bid':
                self._buy_market(quantity)
            elif order_type == 'ask':
                self._sell_market(quantity)

        # Limit order
        elif random_state > .5:
            price = self.draw_price(order_type, spread)
            quantity = self.draw_quantity('limit')
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
        """
        :param market: exchange agent link
        :param cash: number of cash
        :param assets: number of assets
        :param access: number of future dividends informed
        """
        super().__init__(market, cash, assets)
        self.type = 'Fundamentalist'
        self.access = access

    def _evaluate(self):
        """
        Evaluate stock using constant dividend model.
        """
        div = self.market.dividend(self.access)  # expected value of future dividends
        r = self.market.risk_free  # risk-free rate

        perp = div[-1] / r / (1 + r)**(len(div) - 1)  # perpetual payments
        known = sum([div[i] / (1 + r)**(i + 1) for i in range(len(div) - 1)]) if len(div) > 1 else 0
        return known + perp

    def call(self):
        price = round(self._evaluate(), 1)  # fundamental price
        spread = self.market.spread()

        # Cancel all orders
        if len(self.orders) > 5:
            for order in self.orders:
                self._cancel_order(order)

        random_state = random.random()  # determine order type

        if price >= spread['ask']:
            if random_state > .5:
                self._buy_market(Random.draw_quantity('market'))
            else:
                self._sell_limit(Random.draw_quantity('limit'), price + .1)

        elif price <= spread['bid']:
            if random_state > .5:
                self._sell_market(Random.draw_quantity('market'))
            else:
                self._buy_limit(Random.draw_quantity('limit'), price - .1)

        # Inside the spread
        elif spread['ask'] > price > spread['bid']:
            if random_state > .5:
                self._buy_limit(Random.draw_quantity('limit'), price - .1)
            else:
                self._sell_limit(Random.draw_quantity('limit'), price + .1)


class Chartist(Trader):
    """
    Chartist traders are searching for trends in the price movements. In case of three
    consecutive upward (downward) price steps they buy (sell), otherwise they give a new
    order to the limit order book.
    """
    def __init__(self, market: ExchangeAgent, cash: float or int, assets: int = 0, steps: int = 3):
        """
        :param market: exchange agent link
        :param cash: number of cash
        :param assets: number of assets
        :param steps: number of iterations to determine trend
        """
        super().__init__(market, cash, assets)
        self.type = 'Chartist'
        self.steps = steps  # number of steps to determine trend
        self.history = list()  # historical prices of past n steps

    def _trend(self, steps: int) -> (bool, str or None):
        """
        Check whether there is a price trend present. And return what kind of trend:
        'upward' or 'downward'.

        :param steps: number of steps in past to measure trend
        :return: (True - trend or False - no trend, 'upward' or 'downward')
        """
        if len(self.history) > steps:
            upward = list()
            for i in range(steps):
                upward.append(self.history[i] < self.history[i+1])

            downward = list()
            for i in range(steps):
                downward.append(self.history[i] > self.history[i + 1])

            if all(upward):  # upward trend
                return True, 'upward'

            if all(downward):  # downward trend
                return True, 'downward'

        return False, None  # no trend or not enough history

    def call(self):
        """
        If 'steps' consecutive steps of upward (downward) price movements -> buy (sell) market order. If there are no
        such trend, act as random trader placing only limit orders.
        """
        self.history.append(self.market.price())  # Append current price
        if len(self.history) > self.steps + 1:  # Delete oldest price if too many
            self.history.pop(0)

        spread = self.market.spread()
        trend_bool, direction = self._trend(self.steps)

        # Cancel all orders
        if len(self.orders) > 5:
            for order in self.orders:
                self._cancel_order(order)

        # Trend
        if trend_bool:
            if direction == 'upward':
                self._buy_market(Random.draw_quantity('market'))
            elif direction == 'downward':
                self._sell_market(Random.draw_quantity('market'))
        # No Trend
        else:
            random_state = random.random()  # whether bid or ask
            # Buy
            if random_state > .5:
                self._buy_limit(Random.draw_quantity('limit'), spread['bid'] - Random.draw_delta())
            # Sell
            else:
                price = Random.draw_price('ask', spread)
                self._sell_limit(Random.draw_quantity('limit'), spread['ask'] + Random.draw_delta())


class Universalist(Fundamentalist, Chartist):
    """
    Universalist mixes Fundamentalist, Chartist trading strategies, and allows to change from
    one strategy to another.
    """
    def __init__(self, market: ExchangeAgent, cash: float or int, assets: int = 0, access: int = 1, steps: int = 3):
        """
        :param market: exchange agent link
        :param cash: number of cash
        :param assets: number of assets
        :param access: number of future dividends informed
        :param steps: number of iterations to determine trend
        """
        super().__init__(market, cash, assets)
        self.type = 'Chartist' if random.random() > .5 else 'Fundamentalist'  # randomly decide type
        self.access = access  # next n dividend payments known (Fundamentalist)
        self.steps = steps  # number of steps to determine trend (Chartist)
        self.history = list()  # historical prices of past n steps (Chartist)

    def call(self):
        """
        Call one of parents' methods depending on what type it is currently set.
        """
        if self.type == 'Chartist':
            Chartist.call(self)
        elif self.type == 'Fundamentalist':
            Fundamentalist.call(self)

    def change(self):
        """
        Change trader's type and hence trading strategy
        """
        self.type = 'Chartist' if self.type == 'Fundamentalist' else 'Fundamentalist'
        self.history = list()  # need to clear out (it may contain some irrelevant past info)
