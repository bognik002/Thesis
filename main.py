import AgentBasedModel as abm
import matplotlib.pyplot as plt
from tqdm import tqdm


market = abm.ExchangeAgent()
agents = [abm.NoiseTrader(market, 2000, 3) for i in range(10)]

cash = list()
assets = list()
equity = list()
price = list()
for i in tqdm(range(1000)):
    sum_cash = 0
    sum_assets = 0
    sum_equity = 0
    for agent in agents:
        sum_cash += agent.cash
        sum_assets += agent.assets
        sum_equity += agent.equity()
        agent.call()

    cash.append(sum_cash)
    assets.append(sum_assets)
    equity.append(sum_equity)
    price.append(market.price())

plt.plot(price)
plt.show()
plt.plot(cash)
plt.show()
plt.plot(assets)
plt.show()
plt.plot(equity)
plt.show()
