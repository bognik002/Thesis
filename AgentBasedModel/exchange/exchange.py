from AgentBasedModel.utils import Order, OrderList


class ExchangeAgent:
    """
    ExchangeAgent implements automatic orders handling within the order book. It supports limit orders,
    market orders, cancel orders, returns current spread prices and volumes.
    """
    def __init__(self, spread_init, depth=0, price_std=50, quantity_mean=1, quantity_std=1):
        self.order_book = {'bid': OrderList('bid'), 'ask': OrderList('ask')}
        self.name = 'market'

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

    def get_price(self) -> float or None:
        spread = self.spread()
        if spread['bid'] and spread['ask']:
            return (spread['bid'] + spread['ask']) / 2
        return None

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