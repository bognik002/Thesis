from AgentBasedModel.simulator import SimulatorInfo
import AgentBasedModel.utils.math as math
import matplotlib.pyplot as plt


def plot_price(info: SimulatorInfo, spread=False, rolling: int = 1, figsize=(6, 6)):
    plt.figure(figsize=figsize)
    plt.title('Stock Price') if rolling == 1 else plt.title(f'Stock Price (MA {rolling})')
    plt.xlabel('Iterations')
    plt.ylabel('Price')
    plt.plot(range(rolling, len(info.prices)), math.rolling(info.prices, rolling), color='black')
    if spread:
        v1 = [el['bid'] for el in info.spreads]
        v2 = [el['ask'] for el in info.spreads]
        plt.plot(range(rolling, len(v1)), math.rolling(v1, rolling), label='bid', color='green')
        plt.plot(range(rolling, len(v2)), math.rolling(v2, rolling), label='ask', color='red')
    plt.show()


def plot_price_fundamental(info: SimulatorInfo, spread=False, rolling: int = 1, figsize=(6, 6)):
    plt.figure(figsize=figsize)
    if rolling == 1:
        plt.title('Stock Fundamental and Market value')
    else:
        plt.title(f'Stock Fundamental and Market value (MA {rolling})')
    plt.xlabel('Iterations')
    plt.ylabel('Present value')
    if spread:
        v1 = [el['bid'] for el in info.spreads]
        v2 = [el['ask'] for el in info.spreads]
        plt.plot(range(rolling, len(v1)), math.rolling(v1, rolling), label='bid', color='green')
        plt.plot(range(rolling, len(v2)), math.rolling(v2, rolling), label='ask', color='red')
    plt.plot(range(rolling, len(info.prices)), math.rolling(info.prices, rolling), label='market value', color='black')
    plt.plot(range(rolling, len(info.prices)),
             math.rolling([div / info.exchange.risk_free for div in info.dividends], rolling),
             label='fundamental value')
    plt.legend()
    plt.show()


def plot_arbitrage(info: SimulatorInfo, rolling: int = 1, figsize=(6, 6)):
    plt.figure(figsize=figsize)
    if rolling == 1:
        plt.title('Stock Fundamental and Market value difference')
    else:
        plt.title(f'Stock Fundamental and Market value difference (MA {rolling})')
    plt.xlabel('Iterations')
    plt.ylabel('Present value')
    market = info.prices
    fundamental = [div / info.exchange.risk_free for div in info.dividends]
    arbitrage = [fundamental[i] - market[i] for i in range(len(market))]
    plt.plot(range(rolling, len(arbitrage)), math.rolling(arbitrage, rolling), color='black')
    plt.show()


def plot_dividend(info: SimulatorInfo, rolling: int = 1, figsize=(6, 6)):
    plt.figure(figsize=figsize)
    plt.title('Stock Dividend') if rolling == 1 else plt.title(f'Stock Dividend (MA {rolling})')
    plt.xlabel('Iterations')
    plt.ylabel('Dividend')
    plt.plot(range(rolling, len(info.dividends)), math.rolling(info.dividends, rolling), color='black')
    plt.show()


def plot_orders(info: SimulatorInfo, stat: str = 'quantity', rolling: int = 1, figsize=(6, 6)):
    plt.figure(figsize=figsize)
    plt.title('Book Orders') if rolling == 1 else plt.title(f'Book Orders (MA {rolling})')
    plt.xlabel('Iterations')
    plt.ylabel(stat)
    v1 = [v[stat]['bid'] for v in info.orders]
    v2 = [v[stat]['ask'] for v in info.orders]
    plt.plot(range(rolling, len(v1)), math.rolling(v1, rolling), label='bid', color='green')
    plt.plot(range(rolling, len(v2)), math.rolling(v2, rolling), label='ask', color='red')
    plt.legend()
    plt.show()
