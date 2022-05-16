from AgentBasedModel.simulator import SimulatorInfo
import matplotlib.pyplot as plt


def plot_price(info: SimulatorInfo, spread=False, figsize=(6, 6)):
    plt.figure(figsize=figsize)
    plt.title('Stock Market Price')
    plt.xlabel('Iterations')
    plt.ylabel('Price')
    plt.plot(info.prices, color='black')
    if spread:
        plt.plot([el['bid'] for el in info.spreads], label='bid', color='green')
        plt.plot([el['ask'] for el in info.spreads], label='ask', color='red')
    plt.show()


def plot_price_fundamental(info: SimulatorInfo, spread=False, figsize=(6, 6)):
    plt.figure(figsize=figsize)
    plt.title('Stock Market and Fundamental Price')
    plt.xlabel('Iterations')
    plt.ylabel('Price')
    if spread:
        plt.plot([el['bid'] for el in info.spreads], label='bid', color='green')
        plt.plot([el['ask'] for el in info.spreads], label='ask', color='red')
    plt.plot(info.prices, label='market value', color='black')
    plt.plot([div / info.exchange.risk_free for div in info.dividends], label='fundamental value')
    plt.legend()
    plt.show()


def plot_arbitrage(info: SimulatorInfo, figsize=(6, 6)):
    plt.figure(figsize=figsize)
    plt.title('Stock Market and Fundamental Price Difference')
    plt.xlabel('Iterations')
    plt.ylabel('Price')
    market = info.prices
    fundamental = [div / info.exchange.risk_free for div in info.dividends]
    plt.plot([fundamental[i] - market[i] for i in range(len(market))], color='black')
    plt.show()


def plot_dividend(info: SimulatorInfo, figsize=(6, 6)):
    plt.figure(figsize=figsize)
    plt.title('Stock Dividend')
    plt.xlabel('Iterations')
    plt.ylabel('Dividend')
    plt.plot(info.dividends, color='black')
    plt.show()


def plot_orders(info: SimulatorInfo, stat: str = 'quantity', figsize=(6, 6)):
    """
    Plot statistic describing order book

    :param info: SimulatorInfo object
    :param stat: quantity, price mean, price std, volume sum, volume mean, volume std
    :param figsize: figure sizes
    """
    plt.figure(figsize=figsize)
    plt.title(f'Order book {stat}')
    plt.xlabel('Iterations')
    plt.ylabel(stat)
    plt.plot([v[stat]['bid'] for v in info.orders], color='green', label='bid')
    plt.plot([v[stat]['ask'] for v in info.orders], color='red', label='ask')
    plt.legend()
    plt.show()
