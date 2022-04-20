from AgentBasedModel.simulator import SimulatorInfo
from AgentBasedModel.utils.math import mean
import matplotlib.pyplot as plt


def plot_equity(info: SimulatorInfo, figsize=(6, 6)):
    plt.figure(figsize=figsize)
    plt.title('Traders` mean equity')
    plt.xlabel('Iterations')
    plt.ylabel('Mean Equity')
    plt.plot([mean(v.values()) for v in info.equities], color='black')
    plt.show()


def plot_cash(info: SimulatorInfo, figsize=(6, 6)):
    plt.figure(figsize=figsize)
    plt.title('Traders` mean cash')
    plt.xlabel('Iterations')
    plt.ylabel('Mean Cash')
    plt.plot([mean(v.values()) for v in info.cash], color='black')
    plt.show()


def plot_assets(info: SimulatorInfo, figsize=(6, 6)):
    plt.figure(figsize=figsize)
    plt.title('Traders` mean assets')
    plt.xlabel('Iterations')
    plt.ylabel('Mean Assets')
    plt.plot([mean(v.values()) for v in info.assets], color='black')
    plt.show()


def plot_types(info: SimulatorInfo, figsize=(6, 6)):
    plt.figure(figsize=figsize)
    plt.title('Traders` types')
    plt.xlabel('Iterations')
    plt.ylabel('Number of traders')
    for tr_type in ['Random', 'Fundamentalist', 'Chartist']:
        plt.plot([sum([t == tr_type for t in v.values()]) for v in info.types], label=tr_type)
    plt.legend()
    plt.show()


def plot_returns(info: SimulatorInfo, rolling: int = 1, figsize=(6, 6)):
    plt.figure(figsize=figsize)
    plt.title('Traders` mean return')
    plt.xlabel('Iterations')
    plt.ylabel('Mean Return')
    plt.plot(info.returns(rolling), color='black')
    plt.show()
