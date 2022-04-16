from AgentBasedModel.simulator import SimulatorInfo
import matplotlib.pyplot as plt


def plot_fundamental(info: SimulatorInfo, spread=False, figsize=(6, 6)):
    plt.figure(figsize=figsize)
    plt.title('Price')
    plt.xlabel('Iterations')
    plt.ylabel('Price')
    if spread:
        plt.plot([el['bid'] for el in info.spreads], label='bid', color='green')
        plt.plot([el['ask'] for el in info.spreads], label='ask', color='red')
    plt.plot(info.prices, label='market value', color='black')
    plt.plot([div / info.exchange.risk_free for div in info.dividends], label='fundamental value')
    plt.legend()
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


def plot_dividend(info: SimulatorInfo, figsize=(6, 6)):
    plt.figure(figsize=figsize)
    plt.title('Dividend payments')
    plt.xlabel('Iteration')
    plt.ylabel('Dividend')
    plt.plot(info.dividends, color='black')
    plt.show()
