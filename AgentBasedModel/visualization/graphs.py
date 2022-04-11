from AgentBasedModel.simulator import SimulatorInfo
import matplotlib.pyplot as plt


def plot_price(info: SimulatorInfo, figsize=(6, 6)):
    plt.figure(figsize=figsize)
    plt.title('Stock Price')
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


def plot_volatility(info: SimulatorInfo, figsize=(6, 6)):
    plt.figure(figsize=figsize)
    plt.title('Spread size')
    plt.xlabel('Iterations')
    plt.ylabel('Spread size')
    plt.plot(info.spread_sizes, color='black')
    plt.show()


def plot_equity(info: SimulatorInfo, figsize=(6, 6)):
    plt.figure(figsize=figsize)
    plt.title('Agents aggregate equity')
    plt.xlabel('Iterations')
    plt.ylabel('Equity')
    plt.plot(info.equity, color='black')
    plt.show()


def plot_cash(info: SimulatorInfo, figsize=(6, 6)):
    plt.figure(figsize=figsize)
    plt.title('Agents aggregate cash')
    plt.xlabel('Iterations')
    plt.ylabel('Cash')
    plt.plot(info.cash, color='black')
    plt.show()


def plot_assets_qty(info: SimulatorInfo, figsize=(6, 6)):
    plt.figure(figsize=figsize)
    plt.title('Agents aggregate quantity of assets')
    plt.xlabel('Iterations')
    plt.ylabel('Assets quantity')
    plt.plot(info.assets_qty, color='black')
    plt.show()


def plot_assets_value(info: SimulatorInfo, figsize=(6, 6)):
    plt.figure(figsize=figsize)
    plt.title('Agents aggregate value of assets')
    plt.xlabel('Iterations')
    plt.ylabel('Assets value')
    plt.plot(info.assets_value, color='black')
    plt.show()

