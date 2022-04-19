import AgentBasedModel as abm
from AgentBasedModel.visualization import *

exchange = abm.ExchangeAgent(volume=1000)
simulator = abm.Simulator(**{
    'exchange': exchange,
    'traders': [abm.Random(exchange, 2000, 4) for i in range(10)]
})

simulator.simulate(10000)
info = simulator.info

plot_price(info)
