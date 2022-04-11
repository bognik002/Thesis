import AgentBasedModel as abm
from AgentBasedModel.visualization import *

exchange = abm.ExchangeAgent(volume=1000)
simulator = abm.Simulator(**{
    'exchange': exchange,
    'traders': [abm.NoiseTrader(exchange, 2000, 4) for i in range(10)]
})

simulator.simulate(1000)
plot_price(simulator.info)
