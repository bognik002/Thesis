from AgentBasedModel.simulator import SimulatorInfo
from AgentBasedModel.utils.math import mean, rolling
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


def plot_types(info: SimulatorInfo, figsize=(6, 6), roll=None):
    plt.figure(figsize=figsize)
    plt.title('Traders` types')
    plt.xlabel('Iterations')
    plt.ylabel('Number of traders')
    for tr_type in ['Random', 'Fundamentalist', 'Chartist']:
        values = [sum([t == tr_type for t in v.values()]) for v in info.types]
        if values:
            if roll:
                values = rolling(values, roll)
            plt.plot(values, label=tr_type)
    plt.legend()
    plt.show()


def plot_sentiments(info: SimulatorInfo, figsize=(6, 6), roll=None):
    plt.figure(figsize=figsize)
    plt.title('Traders` sentiments')
    plt.xlabel('Iterations')
    plt.ylabel('Number of traders')
    for sentiment in ['optimistic', 'pessimistic']:
        values = [sum([s == sentiment for s in v.values()]) for v in info.sentiments]
        if values:
            if roll:
                values = rolling(values, roll)
            plt.plot(values, label=sentiment)
    plt.legend()
    plt.show()


def plot_returns(info: SimulatorInfo, types=True, roll: int = 1, figsize=(6, 6)):
    plt.figure(figsize=figsize)
    plt.title('Traders` mean return')
    plt.xlabel('Iterations')
    plt.ylabel('Mean Return')
    if not types:
        values = [mean([mean(v.values()) for v in info.returns[i-roll:i]])
                  for i in range(len(info.returns)) if i - roll >= 0]
        plt.plot(values, color='black')
    else:
        for t in ['Random', 'Fundamentalist', 'Chartist']:
            values = list()
            for i in range(len(info.returns)):
                if i - roll >= 0:
                    r_tmp = list()
                    for j, v in enumerate(info.returns[i-roll:i]):
                        for tr_id, r in v.items():
                            if info.types[i-roll + j][tr_id] == t:
                                r_tmp.append(r)
                    if r_tmp:
                        values.append(mean(r_tmp))

            if values:
                plt.plot(values, label=t)
    plt.plot([info.exchange.risk_free] * len(values), color='black', ls='--', alpha=.8)
    if types:
        plt.legend()
    plt.show()
