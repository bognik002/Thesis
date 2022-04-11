from AgentBasedModel.simulator import SimulatorInfo
import matplotlib.pyplot as plt
import pandas as pd


def plot_prices_stat(info: SimulatorInfo, stat, figsize=(6, 6)):
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


def plot_volumes_stat(info: SimulatorInfo, stat, figsize=(6, 6)):
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


def plot_cash_assets(info: SimulatorInfo, figsize=(6, 6)):
    plt.figure(figsize=figsize)
    plt.title('Agents holdings')
    plt.xlabel('Iterations')
    plt.ylabel('Value')
    plt.plot(info.assets_value, label='assets')
    plt.plot(info.cash, label='cash')
    plt.legend()
    plt.show()
