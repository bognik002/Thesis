import AgentBasedModel as abm
from AgentBasedModel.visualization import *

exchange = abm.ExchangeAgent()
simulator = abm.Simulator(**{
    'exchange': exchange,
    'traders': [abm.NoiseTrader(exchange, 2000, 4) for i in range(10)]
})

simulator.simulate(200)

plot_order_quantities(simulator.info)
