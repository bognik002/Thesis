from AgentBasedModel.simulator import SimulatorInfo
from AgentBasedModel.utils.math import mean
import matplotlib.pyplot as plt


def plot_equity(info: SimulatorInfo, trader_type: str = None, figsize=(6, 6)):
    plt.figure(figsize=figsize)
    plt.title('Traders` mean equity')
    plt.xlabel('Iterations')
    plt.ylabel('Mean Equity')
    if trader_type is not None:
        iterations = list()
        values = list()
        for i in range(len(info.types)):  # iterations
            v = [eq for tr_id, eq in info.equities[i].items() if info.types[i][tr_id] == trader_type]
            if v:
                iterations.append(i)
                values.append(mean(v))

        plt.plot(iterations, values, label=trader_type, color='black')
    else:
        for trader_type in ['Random', 'Fundamentalist', 'Chartist']:
            iterations = list()
            values = list()
            for i in range(len(info.types)):  # iterations
                v = [eq for tr_id, eq in info.equities[i].items() if info.types[i][tr_id] == trader_type]
                if v:
                    iterations.append(i)
                    values.append(mean(v))

            plt.plot(iterations, values, label=trader_type)

    plt.legend()
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
    plt.plot(info.returns(rolling=rolling), color='black')
    plt.show()
