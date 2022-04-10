import matplotlib.pyplot as plt
import pandas as pd
from AgentBasedModel.simulator import SimulatorInfo


def plot_price(info: SimulatorInfo, figsize=(6, 6)):
    plt.figure(figsize=figsize)
    plt.title('Price')
    plt.xlabel('Iterations')
    plt.ylabel('Price')
    plt.plot(info.prices, color='black')
    plt.show()


def plot_order_quantities(info: SimulatorInfo, figsize=(6, 6)):
    plt.figure(figsize=figsize)
    plt.title('Quantity of limit orders in book')
    plt.xlabel('Iterations')
    plt.ylabel('Quantity')
    plt.plot([v['bid'] for v in info.orders_quantities], color='green', label='bid')
    plt.plot([v['ask'] for v in info.orders_quantities], color='red', label='ask')
    plt.legend()
    plt.show()


def plot_order_prices_stat(info: SimulatorInfo, stat, figsize=(6, 6)):
    """
    :param stat: mean, q1, q3, std
    """
    plt.figure(figsize=figsize)
    plt.title(f'Price of limit orders in book ({stat})')
    plt.xlabel('Iterations')
    plt.ylabel(stat)
    plt.plot([v['bid'][stat] for v in info.orders_prices], color='green', label='bid')
    plt.plot([v['ask'][stat] for v in info.orders_prices], color='red', label='ask')
    plt.legend()
    plt.show()


def plot_order_volumes_stat(info: SimulatorInfo, stat, figsize=(6, 6)):
    """
    :param stat: sum, mean, q1, q3, std
    """
    plt.figure(figsize=figsize)
    plt.title(f'Volume of limit orders in book ({stat})')
    plt.xlabel('Iterations')
    plt.ylabel(stat)
    plt.plot([v['bid'][stat] for v in info.orders_volumes], color='green', label='bid')
    plt.plot([v['ask'][stat] for v in info.orders_volumes], color='red', label='ask')
    plt.legend()
    plt.show()


def plot_volatility(info: SimulatorInfo, figsize=(6, 6)):
    plt.figure(figsize=figsize)
    plt.title('Spread size')
    plt.xlabel('Iterations')
    plt.ylabel('Spread size')
    plt.plot(info.spread_sizes, color='black')
    plt.show()


def print_order_book(info: SimulatorInfo, n=5):
    val = pd.concat([
        pd.DataFrame({
            'Sell': [v.price for v in info.exchange.order_book['ask']],
            'Quantity': [v.qty for v in info.exchange.order_book['ask']]
            }).groupby('Sell').sum().reset_index().head(n),
        pd.DataFrame({
            'Buy': [v.price for v in info.exchange.order_book['bid']],
            'Quantity': [v.qty for v in info.exchange.order_book['bid']]
        }).groupby('Buy').sum().reset_index().sort_values('Buy', ascending=False).head(n)
    ])
    print(val[['Buy', 'Sell', 'Quantity']].fillna('').to_string(index=False))


def plot_order_book(info: SimulatorInfo, figsize=(6, 6)):
    bid_prices = [v.price for v in info.exchange.order_book['bid']]
    bid_quantities = [v.qty for v in info.exchange.order_book['bid']]
    bid = pd.DataFrame({'Price': bid_prices, 'Volume': bid_quantities}).groupby('Price').sum()
    ask_prices = [v.price for v in info.exchange.order_book['ask']]
    ask_quantities = [v.qty for v in info.exchange.order_book['ask']]
    ask = pd.DataFrame({'Price': ask_prices, 'Volume': ask_quantities}).groupby('Price').sum()

    plt.figure(figsize=(6, 6))
    plt.title('Order book')
    plt.plot(bid, label='bid', color='green')
    plt.plot(ask, label='ask', color='red')
    plt.show()
