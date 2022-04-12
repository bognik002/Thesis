from AgentBasedModel.simulator import SimulatorInfo
import matplotlib.pyplot as plt


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
