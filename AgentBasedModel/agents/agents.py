from AgentBasedModel.exchange import ExchangeAgent
from AgentBasedModel.utils import Order, OrderList


class Trader:
    def __init__(self, market: ExchangeAgent):
        self.market = market
        self.orders = list()
        self.name = 'Undefined'

    def __str__(self) -> str:
        return self.name

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



