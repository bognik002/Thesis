import AgentBasedModel as abm
from AgentBasedModel.visualization import *

exchange = abm.ExchangeAgent(volume=5000)
simulator = abm.Simulator(**{
    'exchange': exchange,
    'traders': [abm.NoiseTrader(exchange, 2000, 4) for i in range(10)]
})

plot_order_book(simulator.info)

simulator.simulate(5000)

plot_order_book(simulator.info)
